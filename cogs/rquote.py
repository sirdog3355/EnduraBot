import os
from dotenv import load_dotenv

load_dotenv()

import discord
from discord.ext import commands
from discord import app_commands, AllowedMentions
from datetime import datetime, timezone, timedelta
import random
import re
import logging
from utils.config_loader import SETTINGS_DATA, MISC_DATA
from utils.logging_setup import COOLDOWN, UNAUTHORIZED
from utils.permissions_checker import check_permissions
from classes.db_rquote_used_handler import RquoteUsed

dupe_blocker = RquoteUsed()

logger = logging.getLogger('endurabot.' + __name__)

GUILD_ID = int(os.getenv('guild'))

def custom_cooldown(interaction: discord.Interaction) -> app_commands.Cooldown | None:

    cog_instance = interaction.client.get_cog('rquote')

    user_role_ids = {role.id for role in interaction.user.roles}

    if not cog_instance.exempt_role_ids.isdisjoint(user_role_ids):
        return None

    if interaction.channel_id == SETTINGS_DATA["quotes_channel_id"]:
        return None

    return app_commands.Cooldown(1, SETTINGS_DATA["rquote_cooldown_in_seconds"])

class rquote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Below 4 class attributes deemed to be useful / necessary.
        self.themes = SETTINGS_DATA["rquote_themes"]
        self.exempt_role_ids = set(SETTINGS_DATA["cooldown_exempt_roles"])
        self.oldest_quote_date = None
        self.misc_data = MISC_DATA

        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True,
                roles=True
            )


    # --- COMMAND: /rquote ---


    @app_commands.command(name="rquote", description="Take an out of context quote and give it the wrong context.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    @app_commands.checks.dynamic_cooldown(custom_cooldown)

    async def rquote(self, interaction: discord.Interaction):

        ooc_channel_id = SETTINGS_DATA["quotes_channel_id"]
        ooc_channel = self.bot.get_channel(ooc_channel_id)

        has_attachment = False

        if interaction.channel.id == ooc_channel_id:
            await interaction.response.send_message("You may not generate quotes in the channel quotes come from.", ephemeral=True)
            logger.log(UNAUTHORIZED, f"{interaction.user.name} ({interaction.user.id}) attempted to generate a quote in #{interaction.channel.name}.")
            return

        # Get date of first ever message in the quotes channel
        if self.oldest_quote_date == None:   
            oldest_msg = [
                msg async for msg in ooc_channel.history(oldest_first=True, limit=1)
            ]
            
            self.oldest_quote_date = oldest_msg[0].created_at

        # Current date - date roughly close to the first quote in #out-of-context
        num_days = datetime.now(timezone.utc) - self.oldest_quote_date

        # This selects the random date
        random_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, num_days.days))

        msg_table = [
            msg async for msg in ooc_channel.history(limit=75, around=random_date)
            if not msg.author.bot
            and (
                (msg.content and (
                    re.search(rf'''{SETTINGS_DATA["rquote_regex"]}''', msg.content)
                ))
            )
            and (
                dupe_blocker.check_status(f"{msg.id}") == False
            )
        ]

        selected_msg = random.choice(msg_table)

        dupe_blocker.add_msg(f"{selected_msg.id}")

        all_matches = re.findall(rf'''{SETTINGS_DATA["rquote_regex"]}''', selected_msg.content)
        extracted_quote = '"\n"'.join(match.strip() for match in all_matches)
        formatted_quote = f'"{extracted_quote}"'

        # Select a random theme and appropriate opening text
        selected_theme_data = self.themes[random.choice(list(self.themes.keys()))]
        opener_key_from_json = selected_theme_data["opener_key"]
        random_opener = random.choice(self.misc_data[opener_key_from_json])

        embed = discord.Embed(
            title=selected_theme_data["title"],
            description=f"{random_opener}\n\n>>> {formatted_quote}",
            color=selected_theme_data["color"]
            )

        embed.set_footer(text=SETTINGS_DATA["rquote_footer"])

        if selected_msg.attachments:
            has_attachment = True
            embed.set_image(url=selected_msg.attachments[0].url)

        await interaction.response.send_message(embed=embed)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) generated a random quote in #{interaction.channel.name} ({interaction.channel.id}).")
        logger.debug(f"{interaction.user.name} ({interaction.user.id}) generated a random quote. Channel: [#{interaction.channel.name} ({interaction.channel.id})]. Dated: [{selected_msg.created_at.strftime("%B %d, %Y")}]. Theme: [{selected_theme_data["title"]}]. Opener: [{random_opener}]. Content: [{formatted_quote}]. Attachment: [{has_attachment}].")

    @rquote.error
    async def rquote_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            minutes, seconds = divmod(int(error.retry_after), 60)
            if minutes > 0:
                await interaction.response.send_message(f"This command is on cooldown. Try again in {minutes} minute(s) and {seconds} second(s).", ephemeral=True)
                logger.log(COOLDOWN, f"{interaction.user.name} ({interaction.user.id}) hit the RQUOTE cooldown with {minutes} minute(s) and {seconds} second(s) remaining.")
            else:
                await interaction.response.send_message(f"This command is on cooldown. Try again in {seconds} second(s).", ephemeral=True)
                logger.log(COOLDOWN, f"{interaction.user.name} ({interaction.user.id}) hit the RQUOTE cooldown with {seconds} second(s) remaining.")


    # --- COMMAND: /rquote-debug ---


    @app_commands.command(name="rquote-debug", description="Debugging tool.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    async def rquote_debug(self, interaction: discord.Interaction, message_id: str):

        # -- Phase 1: Check if channel and message exist --
        channel_id = interaction.channel.id
        channel = self.bot.get_channel(int(channel_id))

        try:
            await channel.fetch_message(int(message_id))
        except discord.NotFound:
            logger.debug(f"{interaction.user.name} ({interaction.user.id}) failed to find message ID ({message_id}) in #{channel.name}.")
            await interaction.response.send_message(f"A message with ID `{message_id}` not found. Note that this command should be run in the channel containing the message.", ephemeral=True)
            return

        # -- Phase 2: Get message in formatted form just like /rquote --

        selected_msg = await channel.fetch_message(int(message_id))
        all_matches = re.findall(rf'''{SETTINGS_DATA["rquote_regex"]}''', selected_msg.content)
        extracted_quote = '"\n"'.join(match.strip() for match in all_matches)
        formatted_quote = f'"{extracted_quote}"'

        if selected_msg.attachments:
            has_attachment = True
            has_attachment_emoji = ":white_check_mark:"
        else:
            has_attachment = False
            has_attachment_emoji = ":x:"

        # -- Phase 3: If the message would never be selected, indicate as such --

        if not all_matches:
            embed1 = discord.Embed(
                title=":x: Message is not qualified",
                description=f"Message does not fit the pattern for quote selection and would not be picked.",
                color=8650752
            )
            embed2 = discord.Embed(
                title=":information_source: Message Information",
                description=f"Message link: {selected_msg.jump_url}",
                color=discord.Color.purple()
            )
            embed2.add_field(name="Author", value=f"<@{selected_msg.author.id}>")
            embed2.add_field(name="Dated", value=f"<t:{round(selected_msg.created_at.timestamp())}:f>")
            embed2.add_field(name="Message ID", value=f"`{selected_msg.id}`")
            embed2.add_field(name="Channel ID", value=f"`{channel_id}`")
            embed2.add_field(name="Qualified", value=":x:")
            embed2.add_field(name="Full Content", value=selected_msg.content, inline=False)
            embed2.add_field(name="Content with Filter", value=formatted_quote, inline=False)
            embed2.add_field(name="Embed", value=has_attachment_emoji)

            if has_attachment == True:
                embed2.set_image(url=selected_msg.attachments[0].url)

            logger.debug(f"{interaction.user.name} ({interaction.user.id}) debugged a message. Verdict: [❌]. Dated: [{selected_msg.created_at.strftime("%B %d, %Y")}]. Message ID: [{selected_msg.id}]. Channel ID: [{channel_id}]. Author: [{selected_msg.author}]. Raw Content: [{selected_msg.content}]. Filtered Content: [{formatted_quote}]. Attachment: [{has_attachment}].")
            await interaction.response.send_message(embeds=[embed1, embed2], ephemeral=True)

        # -- Phase 4: If message WOULD be selected, execute /rquote as normal but with the debugging embed too

        else:

            selected_theme_data = self.themes[random.choice(list(self.themes.keys()))]
            opener_key_from_json = selected_theme_data["opener_key"]
            random_opener = random.choice(self.misc_data[opener_key_from_json])

            embed1 = discord.Embed(
                title=selected_theme_data["title"],
                description=f"{random_opener}\n\n>>> {formatted_quote}",
                color=selected_theme_data["color"]
                )

            embed1.set_footer(text=SETTINGS_DATA["rquote_footer"])

            embed2 = discord.Embed(
                title=":information_source: Message Information",
                description=f"Message link: {selected_msg.jump_url}",
                color=discord.Color.purple()
            )
            embed2.add_field(name="Author", value=f"<@{selected_msg.author.id}>")
            embed2.add_field(name="Dated", value=f"<t:{round(selected_msg.created_at.timestamp())}:f>")
            embed2.add_field(name="Message ID", value=f"`{selected_msg.id}`")
            embed2.add_field(name="Channel ID", value=f"`{channel_id}`")
            embed2.add_field(name="Theme", value=selected_theme_data["opener_key"])
            embed2.add_field(name="Qualified", value=":white_check_mark:")
            embed2.add_field(name="Full Content", value=selected_msg.content, inline=False)
            embed2.add_field(name="Content with Filter", value=formatted_quote, inline=False)
            embed2.add_field(name="Opener", value=random_opener, inline=False)
            embed2.add_field(name="Embed", value=has_attachment_emoji)

            if has_attachment == True:
                embed1.set_image(url=selected_msg.attachments[0].url)

            logger.debug(f"{interaction.user.name} ({interaction.user.id}) debugged a message. Verdict: [✅]. Dated: [{selected_msg.created_at.strftime("%B %d, %Y")}]. Message ID: [{selected_msg.id}]. Channel ID: [{channel_id}]. Author: [{selected_msg.author}]. Theme: [{selected_theme_data["opener_key"]}]. Opener: [{random_opener}]. Raw Content: [{selected_msg.content}]. Filtered Content: [{formatted_quote}]. Attachment: [{has_attachment}].")
            await interaction.response.send_message(embeds=[embed1, embed2], ephemeral=True)

async def setup(bot):
    await bot.add_cog(rquote(bot))