import os
from dotenv import load_dotenv

load_dotenv()

import discord
from discord.ext import commands
from discord import app_commands, AllowedMentions
import logging
import datetime
from utils.config_loader import SETTINGS_DATA
from utils.logging_setup import COOLDOWN
from utils.permissions_checker import check_permissions
from classes.itad_get_games_handler import ItadGameSearchHandler
from classes.itad_get_deals_handler import ItadGameDealsHandler
from classes.custom_exceptions import APIConnectionError, APIContentNotFoundError

logger = logging.getLogger('endurabot.' + __name__)

GUILD_ID = int(os.getenv('guild'))

class game_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.default_allowed_mentions = AllowedMentions(
                everyone=False,
                users=True, 
                roles=True      
            )
        

    # --- COMMAND: /game ---

    @app_commands.command(name="game", description="Get price and identification information for a given video game.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        title = "Game title to search for.",
        private = "Should the output only be visible by you? (default: False)"
    )
    @app_commands.checks.cooldown(SETTINGS_DATA["game_num_uses_before_cooldown"], SETTINGS_DATA["game_cooldown_in_seconds"])

    async def game(self, interaction: discord.Interaction, title: str, private: bool = False):

        itad_name = "[IsThereAnyDeal](https://isthereanydeal.com/)"
    
        if private == False:
            await interaction.response.defer(ephemeral=False)
            hide_state = False
        else:
            await interaction.response.defer(ephemeral=True)
            hide_state = True

        try:
            searched_game = ItadGameSearchHandler(title)
        except APIConnectionError as e:

            api_error_embed = discord.Embed(
            title=":no_entry: API Error",
            description=f"{itad_name} has had an API error: `{e}` \n\n Please notify a <@&{SETTINGS_DATA["sysop_role_id"]}> for investigation.",
            color=8650752
        )

            await interaction.followup.send(embed=api_error_embed)
            logger.error(f"{interaction.user} ({interaction.user.id}) ran /game but IsThereAnyDeal's API had an error: [{e}].")
            return
        
        except APIContentNotFoundError as e:
            
            no_results_embed = discord.Embed(
            title=":wastebasket: No Results",
            description=f"{itad_name} could not find a game with title `{title}`. Please try again.",
            color=discord.Color.purple()
        )
            
            await interaction.followup.send(embed=no_results_embed)
            logger.error(f"{interaction.user} ({interaction.user.id}) ran /game searching for [{title}] and the API returned no results. Error: [{e}] Hide: [{hide_state}]")
            return
        
        game_title = searched_game.get_title()
        game_boxart = searched_game.get_boxart()
        game_uuid = searched_game.get_id()
        game_release = searched_game.get_release_date()
        game_publishers = searched_game.get_publishers()
        game_tags = searched_game.get_tags()
            
        games_to_get_deals = []
        games_to_get_deals.append(game_uuid)

        try:
            game_deals = ItadGameDealsHandler(games_to_get_deals)
        except APIConnectionError as e:   

            api_error_embed = discord.Embed(
            title=":no_entry: API Error",
            description=f"{itad_name} has had an API error: `{e}` \n\n Please notify a <@&{SETTINGS_DATA["sysop_role_id"]}> for investigation.",
            color=8650752
        )

            await interaction.followup.send(embed=api_error_embed)
            logger.error(f"{interaction.user} ({interaction.user.id}) ran /game but IsThereAnyDeal's API had an error: [{e}].")
            return
        except APIContentNotFoundError as e:
            
            no_results_abnormal = discord.Embed(
            title=":interrobang: No Price or Deal Information Found",
            description=f"{itad_name} could not find *any* prices or deals for `{title}`. This is highly unusual given IsThereAnyDeal's purpose. \n\n Please notify a <@&{SETTINGS_DATA["sysop_role_id"]}> for investigation.",
            color=discord.Color.purple()
        )

            await interaction.followup.send(embed=no_results_abnormal)
            logger.error(f"{interaction.user} ({interaction.user.id}) ran /game but IsThereAnyDeal did not return ANY price or deal information for {title} (UUID: {game_uuid}). Error: [{e}] Hide: [{hide_state}]")
            return

        deal = game_deals.get_deals()[0]

        deal_amount = "${:0.2f}".format(deal["deals"][0]["price"]["amount"])
        full_amount = "${:0.2f}".format(deal["deals"][0]["regular"]["amount"])
        shop_raw = f"{deal["deals"][0]["shop"]["name"]}"
        shop_fancy = f"[{deal["deals"][0]["shop"]["name"]}]({deal["deals"][0]["url"]})"
        shop_id = f"{deal["deals"][0]["shop"]["id"]}"
        cut = int(deal["deals"][0]["cut"])

        if cut <= 0:
            custom_description = f"There are no detected deals for *{game_title}*. It can be found at {shop_fancy} for {full_amount}."
            logger.info(f"{interaction.user} ({interaction.user.id}) ran /game for {game_title} (UUID: {game_uuid}) and found no deals. Displayed price was {full_amount} obtained from {shop_raw} (ID: {shop_id}). Hide: [{hide_state}]")
        if cut > 0:
            custom_description = f"*{game_title}* is currently on sale for {cut}% off at {shop_fancy} for {deal_amount}."
            logger.info(f"{interaction.user} ({interaction.user.id}) ran /game for {game_title} (UUID: {game_uuid}) and found a deal. Deal was for {cut}% off at {shop_raw} (ID: {shop_id}) for {deal_amount}. Hide: [{hide_state}]")
        
        embed = discord.Embed(
            title = f"{game_title}",
            color=16777215,
            description=custom_description
        )

        embed.set_image(url=game_boxart)
        embed.add_field(name="Release Date", value=datetime.datetime.strptime(game_release, '%Y-%m-%d').strftime('%B %d, %Y'), inline=False)
        embed.add_field(name="Publishers", value=', '.join(game_publishers), inline=False)
        embed.add_field(name="Tags", value=', '.join(game_tags), inline=False)
        embed.set_footer(text="Powered by the IsThereAnyDeal API.")

        await interaction.followup.send(embed=embed)

    @game.error
    async def game_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            minutes, seconds = divmod(int(error.retry_after), 60)
            if minutes > 0:
                await interaction.response.send_message(f"This command is on cooldown. Try again in {minutes} minute(s) and {seconds} second(s).", ephemeral=True)
                logger.log(COOLDOWN, f"{interaction.user.name} ({interaction.user.id}) hit the GAME cooldown with {minutes} minute(s) and {seconds} second(s) remaining.")
            else:
                await interaction.response.send_message(f"This command is on cooldown. Try again in {seconds} second(s).", ephemeral=True)
                logger.log(COOLDOWN, f"{interaction.user.name} ({interaction.user.id}) hit the GAME cooldown with {seconds} second(s) remaining.")
        

async def setup(bot):
    await bot.add_cog(game_cmd(bot))