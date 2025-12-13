
import os
from dotenv import load_dotenv

load_dotenv()

import requests
import logging

logger = logging.getLogger('endurabot.' + __name__)
API_TOKEN = os.getenv('itad-token')

class ItadGameSearchHandler():
    def __init__(self, title):
        
        base_url_by_name = "https://api.isthereanydeal.com/games/search/v1"
        base_name_payload = {'key': API_TOKEN, 'title': title}
        base_payload = requests.get(base_url_by_name, params=base_name_payload)

        if self.check_connection() == False:
            raise TypeError("API token missing or invalid.")
        
        if not base_payload.json():
            raise ValueError("Game not found.")

        base_data = base_payload.json()[0]

        game_id = base_data["id"]

        full_url = "https://api.isthereanydeal.com/games/info/v2"
        full_payload = {'key': API_TOKEN, 'id': game_id}
        full_response = requests.get(full_url, params=full_payload)

        full_data = full_response.json()

        if not full_data:
            raise ValueError("Something went wrong.")
        
        try:
            self.boxart = full_data["assets"]["boxart"]
        except KeyError:
            self.boxart = None
            logger.debug(f"Boxart not found for {full_data["title"]} ({full_data["id"]}).") 

        if full_data["releaseDate"] == None:
            self.release_date = "Unreleased"
            logger.debug(f"{full_data["title"]}({full_data["id"]}) [releaseDate] set to [Unreleased].")
        else:
            self.release_date = full_data["releaseDate"]

        publisher_list = []
        tags_list = []

        for publisher in full_data["publishers"]:
            publisher_list.append(publisher["name"])

        for tag in full_data["tags"]:
            tags_list.append(tag)

        self.title = full_data["title"]
        self.id = full_data["id"]
        self.publishers = publisher_list
        self.tags = tags_list

    def check_connection(self):
        url = "https://api.isthereanydeal.com/games/lookup/v1"
        payload = {'key': API_TOKEN, 'title': "Verdun"}
        request = requests.get(url, params=payload)

        data = request.json()

        try:
            data["status_code"]
            logger.debug(f"A tested API connection failed.")
            return False
        except KeyError:
            return True
    
    def get_title(self):
        return self.title
    
    def get_boxart(self):
        return self.boxart
    
    def get_id(self):
        return self.id
    
    def get_release_date(self):
        return self.release_date
    
    def get_publishers(self):
        return self.publishers
    
    def get_tags(self):
        return self.tags