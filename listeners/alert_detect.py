import discord
from discord.ext import commands
from discord import AllowedMentions
import logging
import random
from utils.config_loader import SETTINGS_DATA, MISC_DATA

logger = logging.getLogger('endurabot.' + __name__)

class alert_detect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_data = SETTINGS_DATA
        self.misc_data = MISC_DATA        
    
        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True, 
                roles=True      
            )
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
    
        sysop_role_id = self.settings_data.get("sysop_role_id")
        identifiers = self.misc_data.get("issue_identifiers", [])
        servers = self.misc_data.get("server_identifiers", [])

        if not any(role.id == sysop_role_id for role in message.role_mentions):
            return
        
        if any(role.id == sysop_role_id for role in message.author.roles):
           return
        
        if message.author.bot:
            return

        if any(servers in message.content.lower() for servers in servers) and any(identifiers in message.content.lower() for identifiers in identifiers):
            await message.delete()
            embed = discord.Embed(
                title="⚙️ Having an issue? Use `/alert`!", 
                description="An **automated filter** has detected that a recent ping was made to systems operators in relation to an issue with community services.\n\n The preferred method of reporting a service being down is `/alert`.",
                color=8650752
            )
            logger.info(f"{message.author.name} ({message.author.id}) triggered the /alert filter. Content: [{message.content}]")
            await message.channel.send(embed=embed)
        else:
            return
                 
async def setup(bot):
    await bot.add_cog(alert_detect(bot))