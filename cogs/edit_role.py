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
from classes.db_trole_handler import DBTempRole

logger = logging.getLogger('endurabot.' + __name__)

db_temp_role = DBTempRole()

GUILD_ID = int(os.getenv('guild'))

class manage_role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True, 
                roles=True      
            )


    # --- COMMAND: /editrole ---
    
    role_list = SETTINGS_DATA["mod_editable_roles"]
    options_list = []
    for role_name, role_id in role_list.items():
        #Because role ID numbers are so long, it's interpreted as being too big an integer and causes Discord to crash spectacularly. 
        #So need to make it a string using an f-string.
        options_list.append(app_commands.Choice(name=role_name,value=f"{role_id}"))

    @app_commands.command(name="editrole", description="Give or revoke roles indefinitely.")
    @app_commands.check(check_permissions)
    @app_commands.choices(options=options_list)
    @app_commands.guilds(GUILD_ID)
    async def editrole(self, interaction: discord.Interaction, user: discord.Member, options: app_commands.Choice[str], ping: bool = False):

        # And now we make it an integer for the "get_role" method.
        role = interaction.guild.get_role(int(options.value))

        target = interaction.guild.get_member(user.id)

        # Do not mess with the datatype declarations below. They are necessary due to how the SQLITE table is setup.
        if db_temp_role.check_status(str(target.id)) and int(db_temp_role.get_role(str(target.id))) == int(options.value):

            if discord.utils.get(interaction.guild.roles, id=int(db_temp_role.get_role(str(target.id)))) in target.roles:
                await interaction.response.send_message(f"<@{target.id}> was given <@&{options.value}> as a **temporary role** via `/trole`. If you would like to remove it, please use the `remove` arguement of `/trole` instead.", ephemeral=True)
                logger.log(UNAUTHORIZED, f"{interaction.target.name} ({interaction.target.id}) attempted to remove temporary role {options.name} from {target.name} ({target.id}) via /editrole.")
                return

        # Change roles.
        if role in target.roles:
            await target.remove_roles(role)

            embed = discord.Embed(
                title="⭕ Role Removed",
                description=f"{role.mention} has been successfully removed from {target.mention}.",
                color=8650752 
                )
            
            if ping == True:    
                await interaction.response.send_message(embed=embed, content=f"{target.mention}", allowed_mentions=self.default_allowed_mentions)
                logger.info(f"{interaction.target.name} ({interaction.target.id}) removed @{role.name} ({role.id}) from {target.name} ({target.id}). Ping: [TRUE]")
            else:
                await interaction.response.send_message(embed=embed)
                logger.info(f"{interaction.target.name} ({interaction.target.id}) removed @{role.name} ({role.id}) from {target.name} ({target.id}). Ping: [FALSE]")

        else:

            await target.add_roles(role)
            embed = discord.Embed(
                title="🟢 Role Added",
                description=f"{role.mention} has been successfully added to {target.mention}.",
                color=3800852 
                )
            
            if ping == True:    
                await interaction.response.send_message(embed=embed, content=f"{target.mention}", allowed_mentions=self.default_allowed_mentions)
                logger.info(f"{interaction.target.name} ({interaction.target.id}) added @{role.name} ({role.id}) to {target.name} ({target.id}). Ping: [TRUE]")
            else:
                await interaction.response.send_message(embed=embed)
                logger.info(f"{interaction.target.name} ({interaction.target.id}) added @{role.name} ({role.id}) to {target.name} ({target.id}). Ping: [FALSE]")
        
async def setup(bot):
    await bot.add_cog(manage_role(bot))