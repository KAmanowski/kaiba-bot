from discord.ext import commands

import logging

from discord.message import Message

class OnMessageEvent(commands.Cog):
    
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
      
  @commands.Cog.listener()
  async def on_message(self, message: Message):
    splitMessage = message.content.split(' ')
    splitMessage[0] = str.lower(splitMessage[0])
    
    message_content = ""
    
    for part in splitMessage:
      message_content += f"{part} "
      
    message.content = message_content
    
    await self.bot.process_commands(message)
