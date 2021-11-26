from discord.ext import commands
from discord.errors import Forbidden
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

from task.ServerCommandBlockTask import ServerCommandBlockTask
from util.DynamicConfigWriter import DynamicConfigWriter

class HelpCommand(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    def list_available_commands(self):
        commands = []
        commands.append('announce')
        commands.append('book')
        commands.append('help')
        commands.append('parrot')
        commands.append('ping')
        commands.append('rand')
        commands.append('server')
        
        return commands
        
    @commands.command()
    async def help(self, ctx: Context):
        try:
            # Delete calling message
            await ctx.message.delete()
        except Forbidden:
            pass
        
        helpMessage = "```Hello, these are the available commands:\n\n"
        commands = self.list_available_commands()
        
        for command in commands:
            helpMessage += f"{command}\n"
            
        helpMessage += "\nUse £help <command> for specific command help.```"
        
        await ctx.send(helpMessage)
        