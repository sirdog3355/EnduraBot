import os
from dotenv import load_dotenv
from utils.config_loader import SETTINGS_DATA
from classes.custom_exceptions import APIConnectionError, APIContentNotFoundError

load_dotenv()

import requests
import logging

logger = logging.getLogger('endurabot.' + __name__)
API_TOKEN = os.getenv('itad-token')

class ItadGameDealsHandler():
    def __init__(self, deals_list):

        deals_url = "https://api.isthereanydeal.com/games/prices/v3"
        deals_header = {'key': API_TOKEN}
        response = requests.post(deals_url, params=deals_header, json=deals_list)

        prices_data = response.json()

        if not prices_data:
            raise APIContentNotFoundError("Endpoint [/games/prices/v3] returned nothing at all when passed UUIDs.")

        if "status_code" in prices_data and prices_data["status_code"] == 403:
            raise APIConnectionError(f"Endpoint [/games/prices/v3] has rejected EnduraBot's API key.")
        elif "status_code" in prices_data:
            raise APIConnectionError(f"Endpoint [/games/prices/v3] returned status code {prices_data["status_code"]} rather than content.")
        
        self.deals = prices_data
        self.list_of_ids = deals_list

    def get_deals(self):
        deals_sorted_by_first_offer_price = sorted(self.deals, key=lambda x: x['deals'][0]['price']['amount'])

        blacklisted_ids = list(SETTINGS_DATA["blacklisted_itad_shops"].values())

        final_games_with_sorted_deals = [] 
        for game_data in deals_sorted_by_first_offer_price:
            valid_offers = [
                    offer for offer in game_data['deals'] 
                    if offer['shop']['id'] not in blacklisted_ids
                ]
            
            sorted_valid_offers = sorted(valid_offers, key=lambda offer: offer['price']['amount'])
            
            game_data['deals'] = sorted_valid_offers
            final_games_with_sorted_deals.append(game_data)

        deals_cut = list(final_games_with_sorted_deals)
        return deals_cut