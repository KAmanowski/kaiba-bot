from discord.ext import commands
from discord.ext.commands.bot import Bot
import logging
from command.BoysNightCountdownCommand import BoysNightCountdownCommand
from command.CountdownCommand import CountdownCommand

from command.PingCommand import PingCommand
from command.RandCommand import RandCommand
from util.ConfigReader import ConfigReader

def initialiseCommands(bot: Bot):
    bot.add_cog(RandCommand(bot))
    bot.add_cog(PingCommand(bot))
    bot.add_cog(CountdownCommand(bot))
    bot.add_cog(BoysNightCountdownCommand(bot))
    
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='£')

initialiseCommands(bot)
    
bot.run(ConfigReader.getToken())