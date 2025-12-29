import os
from dotenv import load_dotenv

load_dotenv()

import discord
from discord.ext import commands
from discord import app_commands, AllowedMentions
import sys
import logging
import utils.config_loader as config_loader
from utils.config_loader import SETTINGS_DATA, MISC_DATA
from utils.logging_setup import BLACKLIST
from utils.permissions_checker import check_permissions
from classes.db_blacklist_handler import DBBlacklist

db = DBBlacklist()

logger = logging.getLogger('endurabot.' + __name__)

GUILD_ID = int(os.getenv('guild'))

class blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True, 
                roles=True      
            )

    # --- COMMAND: /blacklist ---

    @app_commands.command(name="blacklist", description="Blacklist user from using EnduraBot.")
    @app_commands.check(check_permissions)
    @app_commands.choices(options = [
    app_commands.Choice(name="Add User",value="add"),
    app_commands.Choice(name="Remove User",value="remove")
])
    @app_commands.describe(
        options = "Add or remove user from the blacklist.",
        user = "Member to blacklist."
    )
    @app_commands.guilds(GUILD_ID)
    async def blacklist(self, interaction: discord.Interaction, options: app_commands.Choice[str], user: discord.Member):

        guild_mod_role = discord.utils.get(interaction.guild.roles, id=SETTINGS_DATA["mod_role_id"])
        
        if options.value == "add":

            if user.bot:
                await interaction.response.send_message(f"Bots may not be blacklisted.", ephemeral=True)
                logger.log(BLACKLIST, f"{interaction.user.name} ({interaction.user.id}) attempted to blacklist bot {user.name} ({user.id}).")
                return

            if user.guild_permissions.administrator or guild_mod_role in user.roles:
                await interaction.response.send_message(f"Staff may not be blacklisted. If they warrant blacklisting they should not be staff members.", ephemeral=True)
                logger.log(BLACKLIST, f"{interaction.user.name} ({interaction.user.id}) attempted to blacklist staff member {user.name} ({user.id}).")
                return
            
            try:     
                db.add_user(user.id, interaction.user.id)
                await interaction.response.send_message(f"<@{user.id}> has been successfully blacklisted.", ephemeral=True)
                logger.log(BLACKLIST, f"{interaction.user.name} ({interaction.user.id}) has blacklisted {user.name} ({user.id}) from using EnduraBot.")
            except ValueError:
                await interaction.response.send_message(f"<@{user.id}> is already on the blacklist.", ephemeral=True)
                logger.log(BLACKLIST, f"{interaction.user.name} ({interaction.user.id}) attempted to blacklist {user.name} ({user.id}) from using EnduraBot but they were already blacklisted.")
        
        else:
            
            try:        
                db.remove_user(user.id)
                await interaction.response.send_message(f"<@{user.id}> has been removed from the blacklist.", ephemeral=True)
                logger.log(BLACKLIST, f"{interaction.user.name} ({interaction.user.id}) has removed {user.name} ({user.id}) from the EnduraBot blacklist.")
            except ValueError:
                await interaction.response.send_message(f"<@{user.id}> is already not blacklisted.", ephemeral=True)
                logger.log(BLACKLIST, f"{interaction.user.name} ({interaction.user.id}) attempted to remove {user.name} ({user.id}) from the EnduraBot blacklist but they were already not blacklisted.")

async def setup(bot):
    await bot.add_cog(blacklist(bot))