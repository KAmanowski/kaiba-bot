from os import name
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext import commands
from discord.ext.commands.bot import Bot
from pretty_help import PrettyHelp
from pretty_help.menu import DefaultMenu

from command.AnnounceCommand import AnnounceCommand
from command.BookCommand import BookCommand
from command.ForfeitCommand import ForfeitCommand
from command.ClearCommand import ClearCommand
from command.ParrotCommand import ParrotCommand

from command.PingCommand import PingCommand
from command.RandCommand import RandCommand
from command.ServerCommand import ServerCommand
from provider.Merlin import Merlin
from task.RunCronJobsTask import RunCronJobsTask
from task.ServerCommandBlockTask import ServerCommandBlockTask
from task.ServerStatusRefreshTask import ServerStatusRefreshTask
from util.ConfigReader import ConfigReader

import logging
from rich.logging import RichHandler
import discord

def initialise_commands(bot: Bot):
    bot.add_cog(RandCommand(bot))
    bot.add_cog(PingCommand(bot))
    #bot.add_cog(CountdownCommand(bot))
    bot.add_cog(ServerCommand(bot))
    bot.add_cog(AnnounceCommand(bot))
    bot.add_cog(ParrotCommand(bot))
    bot.add_cog(BookCommand(bot))
    bot.add_cog(ForfeitCommand(bot))
    bot.add_cog(ClearCommand(bot))
    
def initialise_tasks(bot: Bot):
    bot.add_cog(ServerStatusRefreshTask(bot))
    bot.add_cog(ServerCommandBlockTask(bot))
    #bot.add_cog(CountdownTask(bot))
    #bot.add_cog(RunCronJobsTask(bot))
    
def initialise_logger():
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )  # set level=20 or logging.INFO to turn of debug
    
initialise_logger()

menu = DefaultMenu(page_left="👈", page_right="👉", remove="❌", active_time=120, delete_after_timeout=False)

ending_note = "Use £help <command> for more details.\n\nExample: £help server"

bot = commands.Bot(command_prefix='£', help_command=PrettyHelp(menu=menu, sort_commands=True, show_index=True, ending_note=ending_note, index_title="Commands", color=discord.Color.dark_purple()))
bot.activity = Activity(name="your mum | £help", type=ActivityType.watching)
bot.id = 850455972736794664
bot.merlin = Merlin()

initialise_commands(bot)
initialise_tasks(bot)
    
bot.run(ConfigReader.get_token())