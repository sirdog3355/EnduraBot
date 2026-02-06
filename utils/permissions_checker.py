import discord
import logging
from utils.config_loader import PERMS_DATA, SETTINGS_DATA
from classes.db_blacklist_handler import DBBlacklist

logger = logging.getLogger('endurabot.' + __name__)
db = DBBlacklist()

async def check_permissions(interaction: discord.Interaction):

    cmd = interaction.command.name
    eligible_role_ids = PERMS_DATA.get(cmd, [])

    # If user is blacklisted, reject.
    if db.check_status(interaction.user.id) == True:
        return False

    # If command is disabled, reject.
    cmds = SETTINGS_DATA["disabled_cmds"].items()
    for name, reason in cmds:
        if interaction.command.name == name:
            return False
    
    # If no IDs exist, then the command doesn't have a restriction.
    if not eligible_role_ids:
        return True

    eligible_roles_objects = []
    for role_id in eligible_role_ids:
        role = interaction.guild.get_role(role_id)
        if role:
            eligible_roles_objects.append(role)

    user_roles = interaction.user.roles

    if set(eligible_roles_objects).intersection(user_roles):
        return True
    # If user has the native Discord administrator permission, regardless of their roles, permit command use.
    elif not set(eligible_roles_objects).intersection(user_roles) and interaction.user.guild_permissions.administrator:
        logger.debug(f"Administrator {interaction.user.name} ({interaction.user.id}) bypassed traditional restrictions for command /{interaction.command.name}.")
        return True
    else:
        return False
        
