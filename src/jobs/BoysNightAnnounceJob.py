from discord.channel import TextChannel
from discord.ext.commands.bot import Bot
from util.ConfigReader import ConfigReader
import pycron

from util.DynamicConfigWriter import DynamicConfigWriter

class BoysNightAnnounceJob():
    
    SERVER = 'kaiba'
    CHANNEL = 'bantercave'
    CRON_EXPR = '0 21 * * 5'
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.hasPosted = True
        
    async def send_message(self, message: str):
        if self.hasPosted == False:
            self.hasPosted = True
            # Get 'servers' channel in KaibaCorp server
            channel = self.bot.get_channel(ConfigReader.get_channel_id(self.SERVER, self.CHANNEL))
            isinstance(channel, TextChannel)
            
            await channel.send(message)
            
    async def clear_current_bookings(self):
        DynamicConfigWriter.task_migrate_bookings_to_history('yellow')
        DynamicConfigWriter.task_migrate_bookings_to_history('red')
    
    async def run_job(self):
        bot: Bot = self.bot
        
        await bot.wait_until_ready()
        
        if pycron.is_now(self.CRON_EXPR):
            message = f"It's Boys' Night! Time for another night of debauchery!\n"
            message += f""
            await self.send_message(message)
            await self.clear_current_bookings()
        else:
            self.hasPosted = False