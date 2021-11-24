from os import name
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext import commands
from discord.ext.commands.bot import Bot
import logging
from command.AnnounceCommand import AnnounceCommand
from command.BookCommand import BookCommand
from command.ParrotCommand import ParrotCommand

from command.PingCommand import PingCommand
from command.RandCommand import RandCommand
from command.ServerCommand import ServerCommand
from task.RunCronJobsTask import RunCronJobsTask
from task.ServerCommandBlockTask import ServerCommandBlockTask
from task.ServerStatusRefreshTask import ServerStatusRefreshTask
from util.ConfigReader import ConfigReader

def initialise_commands(bot: Bot):
    bot.add_cog(RandCommand(bot))
    bot.add_cog(PingCommand(bot))
    #bot.add_cog(CountdownCommand(bot))
    bot.add_cog(ServerCommand(bot))
    bot.add_cog(AnnounceCommand(bot))
    bot.add_cog(ParrotCommand(bot))
    bot.add_cog(BookCommand(bot))
    
def initialise_tasks(bot: Bot):
    bot.add_cog(ServerStatusRefreshTask(bot))
    bot.add_cog(ServerCommandBlockTask(bot))
    #bot.add_cog(CountdownTask(bot))
    bot.add_cog(RunCronJobsTask(bot))
    
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='£')
bot.activity = Activity(name="your mum | £help", type=ActivityType.watching)
bot.id = 850455972736794664

initialise_commands(bot)
initialise_tasks(bot)
    
bot.run(ConfigReader.get_token())