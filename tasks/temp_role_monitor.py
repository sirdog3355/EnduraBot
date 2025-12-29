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
                user = self.guild.get_member(
                    int(temp_role.get_user_id_by_timestamp(timestamp))
                )
                role = self.guild.get_role(int(temp_role.get_role_by_timestamp(timestamp)))
                if role in user.roles:
                    await user.remove_roles(role)
                    logger.info(
                        f"{temp_role.get_user_name_by_timestamp(timestamp)} ({temp_role.get_user_id_by_timestamp(timestamp)}) was given [@{role.name}] temporarily and the duration has ended. Role removed and status removed from database."
                    )
                    temp_role.remove_user_by_timestamp(timestamp)
                else:
                    logger.info(
                        f"{temp_role.get_user_name_by_timestamp(timestamp)} ({temp_role.get_user_id_by_timestamp(timestamp)}) was given [@{role.name}] temporarily and the duration has ended. Role detected to have been removed early. Removed status from database."
                    )
                    temp_role.remove_user_by_timestamp(timestamp)

    @check_length_minutely.before_loop
    async def before_daily_bible_quote(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(take_l_monitor(bot))
