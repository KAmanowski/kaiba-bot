from discord.ext import commands
from discord.ext.commands.context import Context

from util.ErrorRaiser import ErrorRaiser

class BoysNightCountdownCommand(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command()
    async def boysnight(self, ctx: Context, *args):
      try:
        argsLength = len(args)
        
        if (argsLength < 1):
          await ErrorRaiser.noArguments(ctx)
          return
        
        if args[0] == 'commence':
          if args[1] == 'ctd':
            await ctx.send("egg")
      except:
        ErrorRaiser.catchException()
        raise
          

