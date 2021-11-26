from discord.channel import TextChannel
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message

from task.ServerCommandBlockTask import ServerCommandBlockTask
from util.DynamicConfigWriter import DynamicConfigWriter

class MessageCommand(commands.Cog):
    "£message helps you manage messages in a channel."
    
    help_brief = "You can manage messages more efficiently in a channel, like for example, clearing many automatically."
    help_description = "This command only supports one function right now - clear.\n\n£message clear 2 will clear two of the last messages in the current channel and so on."
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command(name="message", brief=help_brief, description=help_description)
    async def message(self, ctx: Context, function, amount):
        try:
            if not (int(amount) > 0 and int(amount) < 101):
                await ctx.send("Amount must be a number between 1 and 100.")
                return
        except:
            await ctx.send("Give me a number of messages to clear.")
            return
            
        try:
            message: Message = ctx.message
            channel: TextChannel = ctx.channel
            
            if str.lower(function) == 'clear':
                await message.delete()
                
                messages = []
                async for histMessage in channel.history(limit=int(amount)):
                    messages.append(histMessage)
                
                await channel.delete_messages(messages)
            else:
                await ctx.send('Invalid function: ' + function)
            
        except Forbidden as e:
            await ctx.send("I don't have permissions to delete messages in this channel.")
            raise e