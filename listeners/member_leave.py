import logging
from utils.logging_setup import INVITES
import discord
import datetime
from discord.ext import commands, tasks
from utils.config_loader import SETTINGS_DATA

logger = logging.getLogger("endurabot." + __name__)


class member_leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        invite_alert_channel = self.bot.get_channel(SETTINGS_DATA["invite_alert_channel_id"])
        
        embed = discord.Embed(
            title=":wave: User has left.",
            color=discord.Color.red()
        )
        embed.add_field(name="Leaving User", value=f"<@{member.id}> ({member.name} | {member.id})", inline=False)
        embed.add_field(name="Last Joined", value=f"<t:{round(member.joined_at.timestamp())}:f> (<t:{round(member.joined_at.timestamp())}:R>)", inline=False)
    
        logger.info(f"{member.name} ({member.id}) has left the server. Their last join date was {member.joined_at.strftime('%B %d, %Y')}.")

        await invite_alert_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(member_leave(bot))