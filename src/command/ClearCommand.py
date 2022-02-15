from datetime import datetime
import discord
from discord.abc import User
from discord.channel import TextChannel
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message

from task.ServerCommandBlockTask import ServerCommandBlockTask
from util.DynamicConfigWriter import DynamicConfigWriter
from util.Parser import Parser

class ClearCommand(commands.Cog):
    "£clear helps you clear messages in a channel."
    
    help_brief = "You don't have to manually delete tons of messages in a channel anymore (thank you Bailey for the inspiration to make this command)."
    help_description = "This command lets you clear up to 100 messages at once.\n\n\
        £clear 2 will clear two of the last messages in the current channel and so on.\n\n\
        You can also attach a user (via @) on the end to delete just their messages in the past <amount> messages. This is optional."
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command(name="clear", brief=help_brief, description=help_description)
    async def clear(self, ctx: Context, amount, userId=""):
        # Validate amount
        try:
            amount = int(amount)
        except:
            await ctx.send(f"'{amount}' is not a number.")
            return
        
        if not (amount > 0 and amount < 101):
            await ctx.send("Amount must be a number between 1 and 100.")
            return
        
        user: User = None
        
        if userId:
            parsedUserId = Parser.parseUserId(userId)  
            
            try:
                if parsedUserId > 0:
                    user: User = await self.bot.fetch_user(parsedUserId)
            except Forbidden as e:
                await ctx.send("Cannot find the user you've given me.")
                raise e
                    
        try:
            message: Message = ctx.message
            channel: TextChannel = ctx.channel
            
            await message.delete()
            
            messages = []
            async for histMessage in channel.history(limit=int(amount)):
                histMessage: Message = histMessage
                if (datetime.now() - histMessage.created_at).days < 14:
                    if user:
                        if histMessage.author.id == user.id:     
                            messages.append(histMessage)
                    else:
                        messages.append(histMessage)
            
            await channel.delete_messages(messages)
            
        except Forbidden as e:
            await ctx.send("I don't have permissions to delete messages in this channel.")
            raise e
        except Exception as e:
            await ctx.send("Something went wrong.") 
            raise e