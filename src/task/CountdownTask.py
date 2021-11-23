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

class CountdownTicker():
  
  def __init__(self, secondsLeft: int, channelId: int, messageId: int):
      self.secondsLeft = secondsLeft
      self.channelId = channelId
      self.messageId = messageId

class CountdownTask(commands.Cog):
    
    MAX_COMMANDS = 5
    
    task_name = 'countdown'
    
    def __init__(self, bot):
      super().__init__()
      self.bot = bot
      self.ctds = []
      self.isRunning = False
      
    def formatSeconds(self, seconds: int) -> str:
      if seconds is not None:
        d = seconds // (3600 * 24)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if d > 0:
            return '{:02d}D {:02d}H {:02d}m {:02d}s'.format(d, h, m, s)
        elif h > 0:
            return '{:02d}H {:02d}m {:02d}s'.format(h, m, s)
        elif m > 0:
            return '{:02d}m {:02d}s'.format(m, s)
        elif s > 0:
            return '{:02d}s'.format(s)
      return "Time's up you fucks."
      
    def start_countdown(self):
      self.countdown.start()
      self.isRunning = True
      
    def stop_countdown(self):
      self.countdown.stop()
      self.isRunning = False
        
    def add_ctd(self, secondsLeft: int, channelId: int, messageId: int):
      self.ctds.append(CountdownTicker(secondsLeft, channelId, messageId))
      
      if (not self.isRunning):
        self.start_countdown()
        
    @tasks.loop(seconds=1)
    async def countdown(self):
      if len(self.ctds) == 0:
        self.stop_countdown()
        return
      
      i = 0
      for ticker in self.ctds:
        try:
          ticker: CountdownTicker
          print(ticker)
          if (ticker.secondsLeft == 0):
            self.ctds.pop(i)
            continue
          
          ticker.secondsLeft = ticker.secondsLeft - 1
          channel = self.bot.get_channel(ticker.channelId)
          isinstance(channel, TextChannel)
          
          message = await channel.fetch_message(ticker.messageId)
          print("fetched message")
          # If found, edit the existing message
          await message.edit(content=self.formatSeconds(ticker.secondsLeft))
          print("Done")
          i = i + 1
        except discord.NotFound:
          self.ctds.pop(i)
        
        
        
        
        
            