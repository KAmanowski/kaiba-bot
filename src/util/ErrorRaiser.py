from discord.ext.commands.context import Context

from util.ConfigReader import ConfigReader

class ErrorRaiser:
  
  async def raiseError(ctx: Context, message: str) -> None:
    await ctx.send(message)
    
  async def noArguments(ctx: Context) -> None:
    await ctx.send(ConfigReader.get_error_message('noArguments'))
    
  async def catchException(ctx: Context) -> None:
    await ctx.send(ConfigReader.get_error_message('general'))