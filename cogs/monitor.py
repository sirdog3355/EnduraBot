import os
from dotenv import load_dotenv

load_dotenv()

import discord
import datetime
from datetime import timedelta
from discord.ext import commands
from discord import app_commands, AllowedMentions
import sys
import logging
import utils.config_loader as config_loader
from utils.config_loader import SETTINGS_DATA
from classes.db_monitor_handler import DBMonitor
from utils.permissions_checker import check_permissions

logger = logging.getLogger('endurabot.' + __name__)

GUILD_ID = int(os.getenv('guild'))

monitor_db = DBMonitor()

class monitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True,
                roles=True
            )

    @app_commands.command(name="monitor", description="Add someone to be monitored on join.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    @app_commands.choices(level = [
        app_commands.Choice(name="Ban and Send Alert",value="ban"),
        app_commands.Choice(name="Send Alert Only",value="alert")
])
    @app_commands.choices(action = [
        app_commands.Choice(name="Add",value="add"),
        app_commands.Choice(name="Remove",value="remove")
])
    @app_commands.describe(
        disc_id = "The Discord ID of the person to monitor for.",
        action = "What is being done?",
        level = "What should happen if the person joins?",
        name = "The common name of the person.",
        steam_id = "The STEAM ID of the person.",
        reason = "Why is the person being monitored?"
    )
    async def monitor(self, interaction: discord.Interaction, disc_id: str, action: app_commands.Choice[str], level: app_commands.Choice[str] = None, name: str = None, steam_id: str = None, reason: str = None):

        if action.value == "add":

            if monitor_db.check_status(disc_id) == True:
                await interaction.response.send_message("Discord ID is already being monitored.", ephemeral=True)
                logger.error(f"{interaction.user.name} ({interaction.user.id}) attempted to add {monitor_db.get_name(disc_id)} ({disc_id}) when they are already being monitored.")
                return

            monitor_db.add_user(target_disc_id=disc_id, target_name=name, target_steam_id=steam_id, mod_name=f"{interaction.user.name}", mod_disc_id=f"{interaction.user.id}", reason=reason, level=level.value)
            await interaction.response.send_message("Entry successfully added.", ephemeral=True)
            logger.info(f"{interaction.user.name} ({interaction.user.id}) added {name} (Discord: {disc_id} | Steam: {steam_id}) for monitoring at level [{level.value.upper()}].")
            return

        if action.value == "remove":
            if monitor_db.check_status(disc_id) == False:
                await interaction.response.send_message("Discord ID is already not being monitored.", ephemeral=True)
                logger.error(f"{interaction.user.name} ({interaction.user.id}) attempted to remove {disc_id} from monitoring but the ID wasn't found.")
                return

            await interaction.response.send_message("Entry successfully removed.", ephemeral=True)
            logger.info(f"{interaction.user.name} ({interaction.user.id}) removed {monitor_db.get_name(disc_id)} ({disc_id}) from monitoring.")
            monitor_db.remove_user(disc_id)
            return
        
async def setup(bot):
    await bot.add_cog(monitor(bot))