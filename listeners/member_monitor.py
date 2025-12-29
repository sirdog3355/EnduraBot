import logging
from utils.logging_setup import INVITES
import discord
import datetime
from discord.ext import commands, tasks
from utils.config_loader import SETTINGS_DATA
from classes.db_monitor_handler import DBMonitor

logger = logging.getLogger("endurabot." + __name__)

db = DBMonitor()

class member_monitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_data = SETTINGS_DATA

    @commands.Cog.listener()
    async def on_member_join(self, member):

        invite_alert_channel = self.bot.get_channel(SETTINGS_DATA["invite_alert_channel_id"])
        mod_role_id = SETTINGS_DATA["mod_role_id"]
        
        if db.check_status(f"{member.id}") == True:

            name = db.get_name(f"{member.id}")
            steamid = db.get_steamid(f"{member.id}")
            mod_id = db.get_mod_id(f"{member.id}")
            reason = db.get_reason(f"{member.id}")
            level = db.get_level(f"{member.id}").upper()
            timestamp = db.get_timestamp(f"{member.id}")

            if db.get_level(f"{member.id}") == "ban":
                await member.ban(reason="Member is on the member_monitor table with an alert level of BAN.")

                embed = discord.Embed(
                    title=":rotating_light: Member Monitor Triggered",
                    description=f"""`{name}` ({member.id}) joined the server. Upon inspection the user was found on the `member_monitor` table with the `{level}` level. As a result, they have been banned from the server preemptively.
                    \n\n <@{mod_id}> added `{name}` to the monitor on <t:{timestamp}:f> with the reason shown below. Please speak with them for further details.
                    \n\n **This individual must be removed from the `member_monitor` table before unbanning**. They will simply be re-banned otherwise.""",
                    color=15086336
                    )
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.add_field(name="SteamID", value=f"`{steamid}`")

                await invite_alert_channel.send(embed=embed, content=f"<@&{mod_role_id}>")
                logger.info(f"{name} (Discord: {member.id} | Steam: {steamid}) detected to have been placed under monitoring at level [{level}]. {name} banned and alert sent.")
            
            else:

                embed = discord.Embed(
                    title=":warning: Member Monitor Triggered",
                    description=f"""`{name}` ({member.id}) joined the server. Upon inspection the user was found on the `member_monitor` table with the `{level}` level. Nothing has happened as a result; this notice is informational.
                    \n\n <@{mod_id}> added `{name}` to the monitor on <t:{timestamp}:f> with the reason shown below. Please speak with them for further details.""",
                    color=16776960
                    )
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.add_field(name="SteamID", value=f"`{steamid}`")

                await invite_alert_channel.send(embed=embed, content=f"<@&{mod_role_id}>")      
                logger.info(f"{name} (Discord: {member.id} | Steam: {steamid}) detected to have been placed under monitoring at level [{level}]. Alert sent.")      

async def setup(bot):
    await bot.add_cog(member_monitor(bot))
