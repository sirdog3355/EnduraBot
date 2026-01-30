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

class channel_link_cog(commands.Cog):
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

        for key, voice, text in links:
            links_strings.append(f"- <#{voice}> :link: <#{text}> (ID: {key})")

        links_fancy = '\n'.join(links_strings)

        embed = discord.Embed(
            title = "Linked Channels",
            description = links_fancy,
            color = discord.Color.purple()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) generated a list of linked channels.")


    # --- COMMAND: /cl-add ---

    @app_commands.command(name="cl-add", description="Link a voice and text channel together.")
    @app_commands.check(check_permissions)
    @app_commands.describe(
        voice_channel = "Discord ID of the voice channel to link.",
        text_channel = "Discord ID of the text channel to link."
    )
    @app_commands.guilds(GUILD_ID)
    async def cladd(self, interaction: discord.Interaction, voice_channel: str, text_channel: str):
        
        channel_link = DBChannelLink()

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

    # --- COMMAND: /cl-remove ---

    @app_commands.command(name="cl-remove", description="Remove the link between a voice and text channel.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    async def clremove(self, interaction: discord.Interaction, id: str):
        
        channel_link = DBChannelLink()

        try:
            channel_link.get_links_by_key(id)
        except ValueError as e:
            await interaction.response.send_message(e, ephemeral=True)
            logger.error(f"{interaction.user.name} ({interaction.user.id}) got an error when trying to delete a link. Error: [{e}]")
        
        get_channels = channel_link.get_links_by_key(id)

        for voice, text in get_channels:
            txt_channel = self.bot.get_channel(int(text))
            vc_channel = self.bot.get_channel(int(voice))

        channel_link.remove_link(id)

        await interaction.response.send_message(f"**Success**: <#{vc_channel.id}> :broken_chain: <#{txt_channel.id}>.", ephemeral=True)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) removed the link between #{vc_channel.name} ({vc_channel.id}) and #{txt_channel.name} ({txt_channel.id}).")


async def setup(bot):
    await bot.add_cog(channel_link_cog(bot))