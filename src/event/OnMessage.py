from discord.ext import commands

import logging

from discord.message import Message

class OnMessageEvent(commands.Cog):
    
  def __init__(self, bot):
    super().__init__()
    self.bot = bot
      
  @commands.Cog.listener()
  async def on_message(self, message: Message):
    message.content = str.lower(message.content)
    await self.bot.process_commands(message)
