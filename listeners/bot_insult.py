import discord
from discord.ext import commands
from discord import AllowedMentions
import logging
import random
from utils.config_loader import SETTINGS_DATA, MISC_DATA

logger = logging.getLogger('endurabot.' + __name__)

class bot_insult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot     
    
        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True, 
                roles=True      
            )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        chance = SETTINGS_DATA["bot_insult_chance"]

        if self.bot.user.mentioned_in(message):

            value = random.random()

            if value <= chance:
                random_insult = random.choice(MISC_DATA["bot_insults"])
                logger.debug(f"{message.author.name} ({message.author.id}) pinged EnduraBot and triggered an insult at value [{value}]. Insult was [{random_insult}].")
                await message.channel.send(f"{message.author.mention}, {random_insult}", allowed_mentions=self.default_allowed_mentions)
            else:
                logger.debug(f"{message.author.name} ({message.author.id}) pinged EnduraBot and did NOT trigger an insult at value [{value}].")
                return 

async def setup(bot):
    await bot.add_cog(bot_insult(bot))