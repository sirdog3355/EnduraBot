import os
from discord.utils import get
import datetime
from datetime import datetime
from discord.ext import tasks, commands
import logging
from classes.db_trole_handler import DBTempRole
from utils.config_loader import SETTINGS_DATA

logger = logging.getLogger("endurabot." + __name__)

temp_role = DBTempRole()

GUILD_ID = int(os.getenv("guild"))


class take_l_monitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.get_guild(GUILD_ID)
        self.check_length_minutely.start()

    def cog_unload(self):
        self.check_length_minutely.cancel()

    @tasks.loop(minutes=1)
    async def check_length_minutely(self):
        timestamps = temp_role.get_timestamps()

        for timestamp in timestamps:
            if datetime.now() > timestamp:
                continue

            user_id = int(temp_role.get_user_id_by_timestamp(timestamp))
            role_id = int(temp_role.get_role_by_timestamp(timestamp))

            role = self.guild.get_role(role_id)
            if role is None:
                logger.warning(f"Role {role_id} no longer exists. Cleaning DB entry.")
                temp_role.remove_user_by_timestamp(timestamp)
                continue

            member = self.guild.get_member(user_id)

            if member is None or not member.roles:
                try:
                    member = await self.guild.fetch_member(user_id)
                except discord.NotFound:
                    logger.info(
                        f"User [{user_id}] no longer in guild. Cleaning database entry."
                    )
                    temp_role.remove_user_by_timestamp(timestamp)
                    continue

            if role in member.roles:
                try:
                    await member.remove_roles(
                        role,
                        reason="Temporary role duration expired"
                    )
                    logger.info(
                        f"{member} ({user_id}) temp role @{role.name} expired. Role removed."
                    )
                except discord.Forbidden:
                    logger.error(
                        f"Missing permissions to remove @{role.name} from {member} ({member.id})."
                    )
                    continue
                except discord.HTTPException as e:
                    logger.error(
                        f"HTTP error removing @{role.name} from {member} ({member.id}): {e}"
                    )
                    continue
            else:
                logger.info(
                    f"{member} ({user_id}) temp role @{role.name} already removed."
                )

            temp_role.remove_user_by_timestamp(timestamp)


    @check_length_minutely.before_loop
    async def before_daily_bible_quote(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(take_l_monitor(bot))
