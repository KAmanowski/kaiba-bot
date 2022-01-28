import imp
from os import name
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext import commands
from discord.ext.commands.bot import Bot
from pretty_help import PrettyHelp
from pretty_help.menu import DefaultMenu

from command.AnnounceCommand import AnnounceCommand
from command.BookCommand import BookCommand
from command.ClearCommand import ClearCommand
from command.ParrotCommand import ParrotCommand
from command.TequilaCountdown import TequilaCommand

from command.PingCommand import PingCommand
from command.RandCommand import RandCommand
from command.ServerCommand import ServerCommand
from event.OnCommandError import OnCommandError
from event.OnMessage import OnMessageEvent
from provider.Merlin import Merlin

from task.RunCronJobsTask import RunCronJobsTask
from task.ServerCommandBlockTask import ServerCommandBlockTask
from task.ServerStatusRefreshTask import ServerStatusRefreshTask
from task.CountdownTask import CountdownTask
from util.ConfigReader import ConfigReader
from rich.logging import RichHandler

import logging
import sys
import discord

DEV_MODE = (len(sys.argv) > 1 and sys.argv[1] == 'dev')

def initialise_commands(bot: Bot):
    bot.add_cog(RandCommand(bot))
    bot.add_cog(PingCommand(bot))
    #bot.add_cog(CountdownCommand(bot))
    bot.add_cog(ServerCommand(bot))
    bot.add_cog(AnnounceCommand(bot))
    bot.add_cog(ParrotCommand(bot))
    bot.add_cog(BookCommand(bot))
    bot.add_cog(ClearCommand(bot))
    bot.add_cog(TequilaCommand(bot))
    
def initialise_tasks(bot: Bot):
    # Restricted tasks only for live
    if not DEV_MODE:
        bot.add_cog(ServerStatusRefreshTask(bot))
        
    bot.add_cog(ServerCommandBlockTask(bot))
    bot.add_cog(CountdownTask(bot))
    #bot.add_cog(RunCronJobsTask(bot))
    
def initialise_events(bot: Bot):
    bot.add_cog(OnMessageEvent(bot))
    bot.add_cog(OnCommandError(bot))

def initialise_logger():
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )  # set level=20 or logging.INFO to turn of debug
    
initialise_logger()

cmd_prefix = '£'

logging.info(f'DEV MODE: {DEV_MODE}')

# Check environment
if DEV_MODE:
    cmd_prefix = '££'
    
# Help menu setup
menu = DefaultMenu(page_left="👈", page_right="👉", remove="❌", active_time=120, delete_after_timeout=False)
ending_note = "Use £help <command> for more details.\n\nExample: £help server"
 
bot = commands.Bot(command_prefix=cmd_prefix, help_command=PrettyHelp(menu=menu, sort_commands=True, show_index=True, ending_note=ending_note, index_title="Commands", color=discord.Color.dark_purple()))
bot.activity = Activity(name=f"your mum | {cmd_prefix}help", type=ActivityType.watching)
bot.id = 850455972736794664
bot.merlin = Merlin()
bot.dev_mode = DEV_MODE
bot.cmd_prefix = cmd_prefix

initialise_events(bot)
initialise_commands(bot)
initialise_tasks(bot)

@bot.event
async def on_message(message):
    # Needed to stop bot processing commands twice.
    pass
   
bot.run(ConfigReader.get_token())