from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

from task.ServerCommandBlockTask import ServerCommandBlockTask
from util.DynamicConfigWriter import DynamicConfigWriter

class PingCommand(commands.Cog):
    "£ping is a simple ping command."
    
    help_brief = "Simple ping - the bot will respond with 'pong'."
    help_description = "Simple ping - the bot will respond with 'pong'."
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command(name="ping", brief=help_brief, description=help_description)
    async def ping(self, ctx: Context):
        await ctx.send('pong')