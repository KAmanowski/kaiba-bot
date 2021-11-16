from typing import Text, Union
from discord.abc import GuildChannel, PrivateChannel
from discord.channel import TextChannel
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message
from provider.Merlin import Merlin


from util.DynamicConfigReader import DynamicConfigReader
from util.DynamicConfigWriter import DynamicConfigWriter

import discord

class ServerStatusRefreshTask(commands.Cog):
    
    task_name = 'update_server_status_message'
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.update_server_status_message.start()
        
    def get_server_info():
        serverList = Merlin.get_all_server_status()
        out = ""
        
        for server in serverList:
            out += str.upper(server) + ' - '
            
            if serverList[server]['online'] == True:
                out += ':heart:'
            else:
                out += ':broken_heart:'
                
            out += '\n\n'
                
            for credential in serverList[server]['credentials']:
                out += str.upper(credential) + ": " + serverList[server]['credentials'][credential] + "\n"
            
            out += "\n"
                
        return out
        
    @tasks.loop(seconds=10)
    async def update_server_status_message(self):
        bot: Bot = self.bot
        
        await bot.wait_until_ready()
        
        channel = bot.get_channel(DynamicConfigReader.task_get_channel_id(ServerStatusRefreshTask.task_name))

        message: Message = None
        
        try:
            isinstance(channel, TextChannel)
            message = await channel.fetch_message(DynamicConfigReader.task_get_message_id(ServerStatusRefreshTask.task_name))
            await message.edit(content=ServerStatusRefreshTask.get_server_info())
        except discord.NotFound:
            message = await channel.send(ServerStatusRefreshTask.get_server_info())
            DynamicConfigWriter.task_write_message_id(ServerStatusRefreshTask.task_name, message.id)