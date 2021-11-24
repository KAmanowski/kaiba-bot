from os import name
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext import commands
from discord.ext.commands.bot import Bot
from pretty_help import PrettyHelp
from pretty_help.menu import DefaultMenu

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

import logging
import discord

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
    
logging.basicConfig(level=logging.ERROR)

menu = DefaultMenu(page_left="👈", page_right="👉", remove="❌", active_time=120, delete_after_timeout=False)

bot = commands.Bot(command_prefix='£', help_command=PrettyHelp(menu=menu, sort_commands=True, show_index=True, index_title="Commands", color=discord.Color.dark_purple()))
bot.activity = Activity(name="your mum | £help", type=ActivityType.watching)
bot.id = 850455972736794664

initialise_commands(bot)
initialise_tasks(bot)
    
bot.run(ConfigReader.get_token())