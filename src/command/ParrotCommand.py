from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message

class ParrotCommand(commands.Cog):
    "£parrot makes the bot parrot what you say. Not very useful but I was bored."
    
    help_brief = "The Parrot command makes Kaiba parrot what you say. It's basically a shorthand of the £announce command."
    help_description = "£parrot \"message\" makes Kaiba delete your command message and repeat the message you gave it."
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command(name="parrot", brief=help_brief, description=help_description)
    async def parrot(self, ctx: Context, message):
        try:
            # Delete calling message
            await ctx.message.delete()
        except Forbidden:
            # The bot can't delete private messages sent to it - instead send without deleting
            pass
        
        await ctx.send(message)
        