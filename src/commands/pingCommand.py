from discord.ext import commands
from discord.ext.commands.context import Context

class PingCommand(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send('pong')