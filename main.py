import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

import discord
from discord import app_commands
from discord.ext import commands

# Setup logging
import utils.logging_setup as logging_setup
from utils.logging_setup import UNAUTHORIZED
from utils.config_loader import PERMS_DATA, SETTINGS_DATA
from classes.db_blacklist_handler import DBBlacklist
logger = logging_setup.configure_logging()

# Environment variable stuff
BOT_TOKEN= os.getenv('bot_token')
GUILD_ID = int(os.getenv('guild'))

guild_object = discord.Object(id=GUILD_ID)
whitelisted_guild_ids_str = os.getenv('guilds')

# Intents
intents = discord.Intents.default()
intents.members = True         
intents.presences = True        
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)
bot.initial_start_time = None

# Dictionary to store invites
invites = {}

# BlacklistDB connection
db = DBBlacklist()

@bot.event
async def on_guild_join(guild):
    if guild.id != GUILD_ID:
        await guild.leave()
        logger.warning(f"Bot joined unauthorized guild '{guild.name}' (ID: {guild.id}). Leaving...")
        return
    else:
        logger.info(f"Bot joined authorized guild '{guild.name}' (ID: {guild.id}).")

@bot.event
async def on_ready():

    # Load cogs, listeners, and tasks.
    try:
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Loaded cogs.{filename[:-3]}")
    except Exception as e:
        logger.critical("FATAL ERROR: ", e)

    try:
        for filename in os.listdir("listeners"):
            if filename.endswith(".py"):
                await bot.load_extension(f"listeners.{filename[:-3]}")
                logger.info(f"Loaded listeners.{filename[:-3]}")
    except Exception as e:
        logger.critical("FATAL ERROR: ", e)

    try:
        for filename in os.listdir("tasks"):
            if filename.endswith(".py"):
                await bot.load_extension(f"tasks.{filename[:-3]}")
                logger.info(f"Loaded tasks.{filename[:-3]}")
    except Exception as e:
        logger.critical("FATAL ERROR: ", e)  
    
    # Sync slash commands to relevant guild.
    try:
        synced = await bot.tree.sync(guild=guild_object)
        logger.info(f"Synced {len(synced)} commands.")
    except Exception as e:
        logger.critical("FATAL ERROR: ", e)    

    logger.info("Hello, world! I am awake and ready to work!")
    
    # Get time that bot loaded up
    if bot.initial_start_time == None:
        bot.initial_start_time = round(discord.utils.utcnow().timestamp())

    # Get invites at time of bot start
    for guild in bot.guilds:
        invites = await guild.invites()

    bot.invites = invites

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    
    if interaction.response.is_done(): 
        return
    
    if isinstance(error, app_commands.CheckFailure):
            
        if db.check_status(interaction.user.id):

            logger.log(UNAUTHORIZED, f"{interaction.user.name} ({interaction.user.id}) attempted to run /{interaction.command.name} while blacklisted.")

            embed = discord.Embed(
                title=":no_entry: Access denied.",
                description=f"You have been blacklisted from using EnduraBot.",
                color=00000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif interaction.command.name in SETTINGS_DATA["disabled_cmds"]:

            logger.log(UNAUTHORIZED, f"{interaction.user.name} ({interaction.user.id}) attempted to run disabled command /{interaction.command.name}.")

            embed = discord.Embed(
                title=":gear: Command disabled.",
                description=f"Command `/{interaction.command.name}` has been disabled.",
                color=8650752
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        else:

            logger.log(UNAUTHORIZED, f"{interaction.user.name} ({interaction.user.id}) attempted to run /{interaction.command.name}.")
            
            eligible_role_ids = PERMS_DATA.get(interaction.command.name, [])

            embed = discord.Embed(
                title=":octagonal_sign: Access denied.",
                description=f"You do not possess access to run `/{interaction.command.name}`. Only members with the role(s) below may use this command.",
                color=8650752
            )
            embed.add_field(name="Approved Role(s)", value=f"{' | '.join(f"<@&{role_id}>" for role_id in eligible_role_ids)}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

bot.run(BOT_TOKEN)


