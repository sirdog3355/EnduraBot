import os
from dotenv import load_dotenv

load_dotenv()

import discord
from discord.ext import commands
from discord import app_commands, AllowedMentions
import logging
from utils.config_loader import SETTINGS_DATA
from utils.logging_setup import UNAUTHORIZED
from utils.permissions_checker import check_permissions
from classes.db_channel_link_handler import DBChannelLink

logger = logging.getLogger('endurabot.' + __name__)

GUILD_ID = int(os.getenv('guild'))

class channel_link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True, 
                roles=True      
            )

    # --- COMMAND: /cl-list ---

    @app_commands.command(name="cl-list", description="List the channels that are linked together.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    async def cllist(self, interaction: discord.Interaction):
        
        channel_link = DBChannelLink()

        links = channel_link.get_links()
        links_strings = []

        for voice, text in links:
            links_strings.append(f"- <#{voice}> :link: <#{text}>")

        links_fancy = '\n'.join(links_strings)

        embed = discord.Embed(
            title = "Linked Channels",
            description = links_fancy,
            color = discord.Color.purple()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) generated a list of linked channels.")


    # --- COMMAND: /clink ---

    @app_commands.command(name="clink", description="Adjust the linking of channels.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    @app_commands.choices(action = [
        app_commands.Choice(name="Add Link",value="add"),
        app_commands.Choice(name="Remove Link",value="remove")
])
    async def clink(self, interaction: discord.Interaction, action: app_commands.Choice[str], text_channel: str, voice_channel: str):
        
        channel_link = DBChannelLink()
        
        if action.value == "add":
        
            if self.bot.get_channel(int(text_channel)) == None or self.bot.get_channel(int(voice_channel)) == None:
                await interaction.response.send_message("One of the IDs provided is not a channel ID. Please try again.", ephemeral=True)
                logger.error(f"{interaction.user.name} ({interaction.user.id}) attempted to LINK channels but one of them was not a channel ID.")

            txt_channel = self.bot.get_channel(int(text_channel))
            vc_channel = self.bot.get_channel(int(voice_channel))

            try:
                channel_link.add_link(text_channel, voice_channel)
            except ValueError as e:
                await interaction.response.send_message(e, ephemeral=True)
                logger.error(f"{interaction.user.name} ({interaction.user.id}) got an error when trying to LINK #{vc_channel.name} ({vc_channel.id}) and #{txt_channel.name} ({txt_channel.id}): [{e}]")

            await interaction.response.send_message(f"**Success**: <#{vc_channel.id}> :link: <#{txt_channel.id}>", ephemeral=True)
            logger.info(f"{interaction.user.name} ({interaction.user.id}) linked #{vc_channel.name} ({vc_channel.id}) to #{txt_channel.name} ({txt_channel.id})")

        if action.value == "remove":

            if self.bot.get_channel(int(text_channel)) == None or self.bot.get_channel(int(voice_channel)) == None:
                await interaction.response.send_message("One of the IDs provided is not a channel ID. Please try again.", ephemeral=True)
                logger.error(f"{interaction.user.name} ({interaction.user.id}) attempted to DE-LINK channels but one of them was not a channel ID.")

            txt_channel = self.bot.get_channel(int(text_channel))
            vc_channel = self.bot.get_channel(int(voice_channel))

            try:
                channel_link.remove_link(text_channel, voice_channel)
            except ValueError as e:
                await interaction.response.send_message(e, ephemeral=True)
                logger.error(f"{interaction.user.name} ({interaction.user.id}) got an error when trying DE-LINK #{vc_channel.name} ({vc_channel.id}) and #{txt_channel.name} ({txt_channel.id}): [{e}]")
            
            await interaction.response.send_message(f"**Success**: <#{vc_channel.id}> :broken_chain: <#{txt_channel.id}>", ephemeral=True)
            logger.info(f"{interaction.user.name} ({interaction.user.id}) unlinked #{vc_channel.name} ({vc_channel.id}) from #{txt_channel.name} ({txt_channel.id})")


async def setup(bot):
    await bot.add_cog(channel_link(bot))