import os
from dotenv import load_dotenv

load_dotenv()

import discord
import re
from datetime import timedelta
from discord.ext import commands
from discord import app_commands, AllowedMentions
import sys
import logging
from utils.config_loader import SETTINGS_DATA, MISC_DATA
from utils.permissions_checker import check_permissions

logger = logging.getLogger('endurabot.' + __name__)

GUILD_ID = int(os.getenv('guild'))

class user_cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True,
                roles=True
            )

# --- COMMAND: /about ---

    @app_commands.command(name="about", description="Get information about EnduraBot.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    async def about(self, interaction: discord.Interaction):

        repo = SETTINGS_DATA["repo"]
        version = SETTINGS_DATA["version"]
        docs = SETTINGS_DATA["docs"]

        embed = discord.Embed(
            title="About me",
            description=f"Hello! My name is EnduraBot. I am a general purpose bot made for the Endurance Coalition. My creator is <@281589411962028034>.",
            color=discord.Color.blue()
                              )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Version", value=version, inline=False)
        embed.add_field(name="GitHub Repository", value=repo, inline=False)
        embed.add_field(name="Documentation", value=docs, inline=False)
        embed.add_field(name="Uptime", value=f"<t:{self.bot.initial_start_time}:R>")

        await interaction.response.send_message(embed=embed)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) ran /about in #{interaction.channel.name} ({interaction.channel.id}).")

# --- COMMAND: /info ---

    @app_commands.command(name="info", description="Quick access to community relevant information.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    @app_commands.choices(options = [
        app_commands.Choice(name="Links",value="links"),
        app_commands.Choice(name="IP Addresses / Ports",value="ports")
])
    @app_commands.describe(
        options = "What information do you want?"
    )
    async def info(self, interaction: discord.Interaction, options: app_commands.Choice[str]):

        if options.value == "links":

            links_list = SETTINGS_DATA["links"]

            embed = discord.Embed(
                title=f":link: {interaction.guild.name} Links",
                color=discord.Color.purple()
            )

            for url, description in links_list.items():
                embed.add_field(
                    name=description,
                    value=f"[Click me]({url})",
                    inline=False
                )

            await interaction.response.send_message(embed=embed)
            logger.info(f"{interaction.user.name} ({interaction.user.id}) ran /info and asked for LINKS in #{interaction.channel.name} ({interaction.channel.id}).")
            return

        if options.value == "ports":

            ports_list = SETTINGS_DATA["ports"]
            ip = SETTINGS_DATA["ip"]
            url = SETTINGS_DATA["url"]

            embed = discord.Embed(
                title=f":wireless: {interaction.guild.name} IP Addresses",
                description=f"Most services should accept `{url}` as our IP address. Just append the port to the end like usual.\n\n If for some reason that does not work, our *raw* IP is `{ip}`.",
                color=discord.Color.blue()
            )

            for game, port in ports_list.items():
                embed.add_field(
                    name=game,
                    value=port,
                    inline=False
                )

            await interaction.response.send_message(embed=embed)
            logger.info(f"{interaction.user.name} ({interaction.user.id}) ran /info and asked for IP ADDRESSES / PORTS in #{interaction.channel.name} ({interaction.channel.id}).")
            return

# --- COMMAND: /reboot ---

    @app_commands.command(name="reboot", description="Reboot EnduraBot.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    async def reboot(self, interaction: discord.Interaction):

        logger.critical(f"{interaction.user.name} ({interaction.user.id}) rebooted me.")
        await interaction.response.send_message("Rebooting...", ephemeral=True)
        await self.bot.close()
        await os.execv(sys.executable, ['python'] + ['main.py'])

# --- COMMAND: /echo ---

    @app_commands.command(name="echo", description="Make EnduraBot speak.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    async def echo(self, interaction: discord.Interaction, msg: str):

        logger.info(f"{interaction.user.name} ({interaction.user.id}) sent a message as EnduraBot with content [{msg}].")
        await interaction.response.send_message("Message sent.", ephemeral=True)
        await interaction.channel.send(msg)

# --- COMMAND: /logs ---

    @app_commands.command(name="logs", description="Review EnduraBot's logs.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        lines = "Number of log lines to review. (default: 15)"
    )
    async def logs(self, interaction: discord.Interaction, lines: int = 15):

        await interaction.response.defer(ephemeral=True)

        log_file = "logs/endurabot.log"

        chosen_lines = [
            line for line in reversed(list(open(log_file)))
                if not any(re.search(text, line) for text in SETTINGS_DATA["log_text_exclude"])
        ]

        if sum(len(i) for i in chosen_lines[0:lines]) > 4096:
            await interaction.followup.send(content="Number of lines requested exceeds Discord's embed character limit. Please try again.", ephemeral=True)
            logger.error(f"{interaction.user.name} ({interaction.user.id}) attempted to review {lines} line(s) from EnduraBot's logs but the output exceeded Discord's character limit for embeds.")
            return

        embed = discord.Embed(
            title=":notepad_spiral: Logs",
            description=f"```\n{'\n'.join(reversed(chosen_lines[0:lines]))}\n```",
            color=16032240
        )

        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) reviewed the last {lines} line(s) from EnduraBot's logs.")


async def setup(bot):
    await bot.add_cog(user_cmds(bot))