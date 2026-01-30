import discord
from discord.ext import commands
from discord import AllowedMentions
import logging
import random
from classes.db_channel_link_handler import DBChannelLink

channel_link = DBChannelLink()

logger = logging.getLogger('endurabot.' + __name__)

class channel_link_listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot     
    
        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True, 
                roles=True      
            )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        # Initiate logic if user joins a linked channel
        if not after.channel == None and channel_link.check_status(after.channel.id) == True:
        
            txt_channel_id = channel_link.get_text_id(after.channel.id)
            txt_channel = self.bot.get_channel(int(txt_channel_id))

            if member.guild_permissions.administrator:
                logger.debug(f"{member.name} ({member.id}) joined VC {after.channel.name} linked to #{txt_channel.name}. {member.name} is an administrator. Nothing to do.")
                return

            # If the user already has a role that can see the linked channel, do nothing.
            for role in member.roles:
                perms = txt_channel.permissions_for(role)

                if perms.read_messages:
                    logger.debug(f"{member.name} ({member.id}) joined VC {after.channel.name} linked to #{txt_channel.name}. {member.name} has role [@{role}] which grants read permissions. Nothing to do.")
                    return

            # If the user still has overwrites in the channel, do nothing.
            if member in txt_channel.overwrites:
                logger.debug(f"{member.name} ({member.id}) joined VC {after.channel.name} linked to #{txt_channel.name}. {member.name} already has overwrites. Nothing to do.")
                return

            # Give them read permissions.
            await txt_channel.set_permissions(member, read_messages=True)
            logger.debug(f"{member.name} ({member.id}) joined VC {after.channel.name} linked to #{txt_channel.name}. Read permissions granted.")

        # If the user moved from another channel or left a channel, and they have overwrites, strip them.
        if not before.channel == None and channel_link.check_status(before.channel.id) == True:
            before_txt_channel_id = channel_link.get_text_id(before.channel.id)
            before_txt_channel = self.bot.get_channel(int(before_txt_channel_id))

            if member in before_txt_channel.overwrites:
                await before_txt_channel.set_permissions(member, overwrite=None)
                logger.debug(f"{member.name} ({member.id}) left VC {before.channel.name} linked to #{before_txt_channel.name}. Read permissions revoked.")
        

async def setup(bot):
    await bot.add_cog(channel_link_listener(bot))