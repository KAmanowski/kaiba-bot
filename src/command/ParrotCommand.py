from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message

class ParrotCommand(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command()
    async def parrot(self, ctx: Context, *args):
        try:
            message: Message = ctx.message
            await message.delete()
            if len(args) > 0:
                await ctx.send(args[0])
        except Forbidden:
            await ctx.send("I cannot parrot your message - I do not have the necessary permissions.")