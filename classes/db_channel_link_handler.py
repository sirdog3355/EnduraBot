import sqlite3
from dotenv import load_dotenv

load_dotenv()

import logging
import datetime
from datetime import datetime

logger = logging.getLogger("endurabot." + __name__)


class DBChannelLink:
    def __init__(self):
        self.connection = sqlite3.connect("endurabot.db")
        self.cursor = self.connection.cursor()
        check_if_table_exists = """CREATE TABLE IF NOT EXISTS channel_link(channel_link_id INTEGER PRIMARY KEY AUTOINCREMENT, text_channel_id TEXT, voice_channel_id TEXT)"""
        self.cursor.execute(check_if_table_exists)
        self.connection.commit()

    def check_status(self, id):

        id = str(id)

        self.cursor.execute("SELECT text_channel_id FROM channel_link")
        tuple = self.cursor.fetchall()
        list = [ints[0] for ints in tuple]

        if id in list:
            return True

        self.cursor.execute("SELECT voice_channel_id FROM channel_link")
        tuple2 = self.cursor.fetchall()
        list2 = [ints[0] for ints in tuple2]

        if id in list2:
            return True

        return False
        
    def add_link(self, text_id, voice_id):

        if self.check_status(text_id) == True:
            raise ValueError("Link already exists for text channel.")

        if self.check_status(voice_id) == True:
            raise ValueError("Link already exists for voice channel.")

        self.cursor.execute("INSERT INTO channel_link(text_channel_id, voice_channel_id) VALUES (?, ?)", (text_id, voice_id,))
        self.connection.commit()

    def remove_link(self, key):

        self.cursor.execute(f"DELETE FROM channel_link WHERE channel_link_id = ?", (key,))
        self.connection.commit()

    def get_text_id(self, voice_id):

        voice_id = str(voice_id)

        self.cursor.execute("SELECT text_channel_id FROM channel_link WHERE voice_channel_id = ?", (voice_id,))
        result = self.cursor.fetchone()
        return result[0]

    def get_links(self):
        self.cursor.execute("SELECT channel_link_id, voice_channel_id, text_channel_id FROM channel_link")
        result = self.cursor.fetchall()
        return result

    def get_links_by_key(self, key):
        self.cursor.execute("SELECT voice_channel_id, text_channel_id FROM channel_link WHERE channel_link_id = ?", (key,))
        result = self.cursor.fetchall()

        if not result:
            raise ValueError("No link found for provided ID.")

        return result

