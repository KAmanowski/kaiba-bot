from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

from task.ServerCommandBlockTask import ServerCommandBlockTask
from util.DynamicConfigWriter import DynamicConfigWriter

class PingCommand(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx: Context):
        DynamicConfigWriter.task_migrate_bookings_to_history('yellow')
        DynamicConfigWriter.task_migrate_bookings_to_history('red')
        await ctx.send('pong')