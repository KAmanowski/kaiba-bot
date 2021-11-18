from typing import Text, Union
from discord.abc import GuildChannel, PrivateChannel
from discord.channel import TextChannel
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message
from provider.Merlin import Merlin
from exception.MerlinErrorException import MerlinErrorException


from util.DynamicConfigReader import DynamicConfigReader
from util.DynamicConfigWriter import DynamicConfigWriter

import discord

class ServerCommandBlockTask(commands.Cog):
    
    MAX_COMMANDS = 5
    
    task_name = 'remove_server_command_blocks'
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.counters: dict = {}
        self.remove_server_command_blocks.start()
        
    def update_counter(self, userId: str):
        if userId in self.counters:
            self.counters[userId] = self.counters[userId] + 1
        else:
            self.counters[userId] = 1
        
    def can_use_command(self, userId: str) -> bool:
        if userId in self.counters:
            if self.counters[userId] >= self.MAX_COMMANDS:
                return False
            else:
                return True
        else:
            return True
        
    @tasks.loop(minutes=15)
    async def remove_server_command_blocks(self):
        self.counters = {}
        
            