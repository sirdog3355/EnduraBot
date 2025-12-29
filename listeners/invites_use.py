import logging
from utils.logging_setup import INVITES
import discord
import datetime
from discord.ext import commands, tasks
from utils.config_loader import SETTINGS_DATA

logger = logging.getLogger("endurabot." + __name__)


def find_invite_by_code(invite_list, code):
    for inv in invite_list:
        if inv.code == code:
            return inv


class invites_use(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        invites_before_join = self.bot.invites
        invites_after_join = await member.guild.invites()

        for invite in invites_before_join:
            if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:

                logger.log(
                    INVITES,
                    f"{member.name} ({member.id}) has joined with invite [{invite.code}] created by {invite.inviter} ({invite.inviter.id}) on {invite.created_at.strftime('%B %d, %Y')}.",
                )

                invite_alert_channel = self.bot.get_channel(SETTINGS_DATA["invite_alert_channel_id"])

                embed = discord.Embed(
                    title=":incoming_envelope: User has joined.",
                    color=3800852
                )
                embed.add_field(name="Joining User", value=f"<@{member.id}> ({member.name} | {member.id})", inline=False)
                embed.add_field(name="Invite Code", value=f"``{invite.code}``", inline=False)
                embed.add_field(name="Invite Creator", value=f"<@{invite.inviter.id}> ({invite.inviter} | {invite.inviter.id})", inline=False)
                embed.add_field(name="Invite Creation Date", value=f"<t:{round(invite.created_at.timestamp())}:f> (<t:{round(invite.created_at.timestamp())}:R>)", inline=False)

                await invite_alert_channel.send(embed=embed)

                self.bot.invites = invites_after_join

                return


async def setup(bot):
    await bot.add_cog(invites_use(bot))
