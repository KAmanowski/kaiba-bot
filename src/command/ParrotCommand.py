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
            # Delete calling message
            await ctx.message.delete()
            if len(args) > 0:
                # Send message bot was told to parrot
                await ctx.send(args[0])
        except Forbidden:
            # The bot can't delete private messages sent to it - the below is sent in this case
            await ctx.send("I cannot parrot your message - I do not have the necessary permissions.")