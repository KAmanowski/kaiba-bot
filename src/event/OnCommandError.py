from discord.ext import commands

import logging
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandError

from discord.message import Message

class OnCommandError(commands.Cog):
    
    def __init__(self, bot):
      super().__init__()
      self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
      """A global error handler cog."""

      if isinstance(error, commands.CommandNotFound):
          message = f"This command does not exist."
      elif isinstance(error, commands.CommandOnCooldown):
          message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
      elif isinstance(error, commands.MissingPermissions):
          message = "You are missing the required permissions to run this command!"
      elif isinstance(error, commands.UserInputError):
          message = "Something about your input was wrong, please check your input and try again."
      else:
          message = f"Ah shit - something went wrong while running the command. <@!{self.bot.creator_id}>"

      await ctx.send(message, delete_after=5)
      await ctx.message.delete(delay=5)
