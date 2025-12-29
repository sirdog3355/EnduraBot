
from datetime import time, timezone
from discord.ext import tasks, commands
import logging
import datetime
from utils.config_loader import SETTINGS_DATA
from utils.logging_setup import BOOT

logger = logging.getLogger('endurabot.' + __name__)

class log_daily_reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_daily_reset_func.start()

    def cog_unload(self):
        self.log_daily_reset_func.cancel()

    @tasks.loop(time=time(hour=SETTINGS_DATA["log_new_day_hour_utc"], minute=0, tzinfo=timezone.utc))
    async def log_daily_reset_func(self):
        await self.bot.wait_until_ready()

        now = datetime.datetime.now()
        boot_message = f"--- {now.strftime('%A, %B %d, %Y (%Y%m%d)')} | {now.strftime('%H:%M')} ---"
        logger.log(BOOT, boot_message)
    
    @log_daily_reset_func.before_loop
    async def before_daily_reset(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(log_daily_reset(bot))