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

    def check_status(self, text_id):
        self.cursor.execute("SELECT text_channel_id FROM channel_link")
        tuple = self.cursor.fetchall()
        list = [ints[0] for ints in tuple]

        if text_id in list:
            return True
        else:
            return False

    def add_link(self, text_id, voice_id):

        text_id = str(text_id)
        voice_id = str(voice_id)

        text_channel = self.bot.get_channel(int(text_id))
        voice_channel = self.bot.get_channel(int(voice_id))

        if text_channel == None or voice_channel == None:
            raise TypeError("One of the provided IDs is not a channel")

        self.cursor.execut("INSERT INTO channel_link(text_channel_id, voice_channel_id) VALUES (?, ?)", (text_id, voice_id,))
        self.connection.commit()

    def get_text_id(self, voice_id):
        self.cursor.execute("SELECT text_channel_id FROM channel_link WHERE voice_channel_id = ?", (voice_id,))
        result = self.cursor.fetchone()
        return result[0]

    def get_voice_id(self, text_id):
        self.cursor.execute("SELECT voice_channel_id FROM channel_link WHERE text_channel_id = ?", (text_id,))
        result = self.cursor.fetchone()
        return result[0]

    def get_links(self):
        self.cursor.execute("SELECT voice_channel_id, text_channel_id FROM channel_link")
        result = self.cursor.fetchall()
        return result