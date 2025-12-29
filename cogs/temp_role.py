import os
from dotenv import load_dotenv

load_dotenv()

import discord
import datetime
from datetime import timedelta
from discord.ext import commands
from discord import app_commands, AllowedMentions
import logging
from utils.config_loader import SETTINGS_DATA, MISC_DATA
from classes.db_trole_handler import DBTempRole
from utils.logging_setup import UNAUTHORIZED
from utils.permissions_checker import check_permissions

logger = logging.getLogger('endurabot.' + __name__)

GUILD_ID = int(os.getenv('guild'))

db_temp_role = DBTempRole()

class temp_role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True,
                roles=True
            )

    role_list = SETTINGS_DATA["mod_editable_roles"]
    options_list = []
    for role_name, role_id in role_list.items():
        #Because role ID numbers are so long, it's interpreted as being too big an integer and causes Discord to crash spectacularly.
        #So need to make it a string using an f-string.
        options_list.append(app_commands.Choice(name=role_name,value=f"{role_id}"))

    @app_commands.command(name="trole", description="Give a user a role temporarily.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    @app_commands.choices(roles=options_list)
    @app_commands.describe(
        target = "Who is the target?",
        length = "Length, in hours, the role should last for. (default: 24)",
        roles = f"Which role should be given to the target? (default: {options_list[0].name})",
        disconnect = "Should the target be disconnected from VC? (default: True)",
        check = "If true, will ONLY be told if there's an active timer for the target.",
        remove = "If true, will ONLY remove the temp role and delete timer for target."
    )
    async def trole(self, interaction: discord.Interaction, target: discord.Member, roles: str = options_list[0].value, length: int = 24, check: bool = False, remove: bool = False, disconnect: bool = True):

        await interaction.response.defer(ephemeral=True)

        role = interaction.guild.get_role(int(roles))
        general_chat = self.bot.get_channel(SETTINGS_DATA["general_chat_channel_id"])
        timestamp_equation = datetime.datetime.now() + timedelta(hours=length)
        timestamp = timestamp_equation.replace(microsecond=0)
        timestamp_fancy = timestamp.strftime("%B %d, %Y %H:%M")
        epoch = round(timestamp_equation.timestamp())

        if check == True:
            if db_temp_role.check_status(str(target.id)) == False:
                await interaction.followup.send(f"<@{target.id}> does not have a temporary role.", ephemeral=True)
                logger.info(f"{interaction.user.name} ({interaction.user.id}) checked if {target.name} ({target.id}) has a temporary role. [FALSE]")
                return
            else:
                timestamp = db_temp_role.check_time(str(target.id))
                mod_id =  db_temp_role.get_mod(str(target.id))
                role_id = db_temp_role.get_role(str(target.id))
                role_name = interaction.guild.get_role(int(role_id)).name
                await interaction.followup.send(f"<@{mod_id}> gave <@&{role_id}> to <@{target.id}>. It is set to be removed <t:{timestamp}:f> (<t:{timestamp}:R>)", ephemeral=True)
                logger.info(f"{interaction.user.name} ({interaction.user.id}) checked if {target.name} ({target.id}) has a temporary role. [TRUE] [@{role_name}]")
                return

        if remove == True:
            if db_temp_role.check_status(str(target.id)) == False:
                await interaction.followup.send(f"<@{target.id}> does not have a temporary role.", ephemeral=True)
                logger.info(f"{interaction.user.name} ({interaction.user.id}) attempted to remove a temporary role from {target.name} ({target.id}) when they did not have one.")
                return
            else:
                role_to_remove = interaction.guild.get_role(int(db_temp_role.get_role(str(target.id))))
                role_name = role_to_remove.name
                await target.remove_roles(role_to_remove)
                await interaction.followup.send(f"<@{target.id}>'s temporary role successfully removed.", ephemeral=True)
                logger.info(f"{interaction.user.name} ({interaction.user.id}) removed the temporary role [@{role_name}] for {target.name} ({target.id}) early.")
                db_temp_role.remove_user_by_id(str(target.id))
                return

        if target.bot:
            await interaction.followup.send("Bots may not be given a temporary role.", ephemeral=True)
            logger.log(UNAUTHORIZED, f"{interaction.user.name} ({interaction.user.id}) tried to give a temporary role to bot {target.name} ({target.id}).")
            return

        if length <= 0:
            await interaction.followup.send("Hilarious.", ephemeral=True)
            return

        if db_temp_role.check_status(str(target.id)) == True:

            db_role = interaction.guild.get_role(int(db_temp_role.get_role(str(target.id))))
            new_role = role

            if not new_role in target.roles:
                await target.remove_roles(db_role)
                await target.add_roles(new_role)

        else:

            await target.add_roles(role)

        db_temp_role.add_user(target.id, target.name, interaction.user.id, interaction.user.name, roles, timestamp)

        if target.voice and disconnect == True:
            await target.move_to(None)

        embed_executor = discord.Embed(
            title="Action successful.",
            description=f"<@{target.id}> given <@&{roles}>.\n\n If you would like to remove the role early use the remove argument in `/trole`.\n\n Running the command again will result in resetting the timer and replacing the temporary role with whatever the new selection is.",
            color=3800852)

        embed_notification_public = discord.Embed(
        title=f"You have been given a temporary role.",
        description=f"<@{interaction.user.id}> has given you the role `@{role.name}`.\n\n The date and time below is when the role will be removed automatically. Note that the removal time may be off by upto 2-5 minutes.",
        color=15277667)
        embed_notification_public.add_field(name="Automatic Removal Time", value=f"<t:{epoch}:f> (<t:{epoch}:R>)", inline=False)

        await general_chat.send(embed=embed_notification_public, content=f"<@{target.id}>", allowed_mentions=self.default_allowed_mentions)

        logger.info(f"{interaction.user.name} ({interaction.user.id}) gave [@{role.name}] to {target.name} ({target.id}) for {length} hour(s). Removal scheduled for {timestamp_fancy}.")
        await interaction.followup.send(embed=embed_executor, ephemeral=True)

async def setup(bot):
    await bot.add_cog(temp_role(bot))