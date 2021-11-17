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
        # Gets status of all servers from Merlin
        serverList = Merlin.get_all_server_status()
        out = ""
        
        # Builds server message
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
        
        # If bot is just started up, wait until it's ready
        await bot.wait_until_ready()
        
        # Get 'servers' channel in KaibaCorp server
        channel = bot.get_channel(DynamicConfigReader.task_get_channel_id(ServerStatusRefreshTask.task_name))

        message: Message = None
        
        try:
            isinstance(channel, TextChannel)
            # Fetch message with last known ID
            message = await channel.fetch_message(DynamicConfigReader.task_get_message_id(ServerStatusRefreshTask.task_name))
            # If found, edit the existing message
            await message.edit(content=ServerStatusRefreshTask.get_server_info())
        except discord.NotFound:
            # If the server message was deleted and thus can't be found, just send a new one
            message = await channel.send(ServerStatusRefreshTask.get_server_info())
            # Save the Id of the new message to update for next iteration of this task in 10 seconds
            DynamicConfigWriter.task_write_message_id(ServerStatusRefreshTask.task_name, message.id)