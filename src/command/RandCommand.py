import discord.ext.commands
import discord
from discord.ext import commands
import random

from discord.ext.commands.context import Context

from util.ErrorRaiser import ErrorRaiser


class RandCommand(commands.Cog):
    "£rand gives you a random number/decimal."
    
    help_brief = "£rand gives you a decimal between 0 and 1. Use £help rand for more arguments."
    help_description = "£rand gives you a decimal between 0 and 1.\n\n \
        £rand n will give a number from 0 to n.\n\n \
        £rand n m will give a number from n to m."
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @commands.command(name="rand", brief=help_brief, description=help_description)
    async def rand(self, ctx: Context, *args):
        member: discord.Member = ctx.author
        argLen = len(args)
        
        validArgs = True
        
        # Checks that each argument given is an integer
        for i in args:
            try:
                int(i)
            except ValueError:
                await ErrorRaiser.raiseError(ctx, member.display_name + ", one of your arguments isn't a number you fucking idiot.")
                validArgs = False
        
        # If all arguments are valid, do one of the below        
        if (validArgs):
            if (argLen == 0):  
                await ctx.send(str(random.random()))
            elif (argLen == 1):
                await ctx.send(str(random.randint(0, int(args[0]))))
            else:
                await ctx.send(str(random.randint(int(args[0]), int(args[1]))))