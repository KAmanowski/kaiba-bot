from discord.ext import commands
from discord.ext.commands.bot import Bot
import logging
from command.AnnounceCommand import AnnounceCommand
from command.BoysNightCountdownCommand import BoysNightCountdownCommand
from command.CountdownCommand import CountdownCommand

from command.PingCommand import PingCommand
from command.RandCommand import RandCommand
from command.ServerCommand import ServerCommand
from task.ServerStatusRefreshTask import ServerStatusRefreshTask
from util.ConfigReader import ConfigReader

def initialise_commands(bot: Bot):
    bot.add_cog(RandCommand(bot))
    bot.add_cog(PingCommand(bot))
    bot.add_cog(CountdownCommand(bot))
    bot.add_cog(BoysNightCountdownCommand(bot))
    bot.add_cog(ServerCommand(bot))
    bot.add_cog(AnnounceCommand(bot))
    
def initialise_tasks(bot: Bot):
    bot.add_cog(ServerStatusRefreshTask(bot))
    
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='£')

initialise_commands(bot)
initialise_tasks(bot)
    
bot.run(ConfigReader.getToken())