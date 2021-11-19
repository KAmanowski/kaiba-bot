from discord.channel import TextChannel
from discord.ext.commands.bot import Bot
from util.ConfigReader import ConfigReader
import pycron

class BoysNightAnnounceJob():
    
    SERVER = 'kaiba'
    CHANNEL = 'bantercave'
    CRON = '0 21 * * 5'
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.hasPosted = True
        
    async def sendMessage(self, message: str):
        if self.hasPosted == False:
            self.hasPosted = True
            # Get 'servers' channel in KaibaCorp server
            channel = self.bot.get_channel(ConfigReader.get_channel_id(self.SERVER, self.CHANNEL))
            isinstance(channel, TextChannel)
            
            await channel.send(message)
    
    async def run_job(self):
        bot: Bot = self.bot
        
        await bot.wait_until_ready()
        
        if pycron.is_now(self.CRON):
            await self.sendMessage("It's Boys' Night!")
        else:
            self.hasPosted = False