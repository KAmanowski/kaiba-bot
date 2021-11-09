import discord.ext.commands
import discord
from discord.ext import commands
import random

from discord.ext.commands.context import Context

from util.ErrorRaiser import ErrorRaiser


class RandCommand(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    
    @commands.command(brief='Gives you a random number.', description='[£rand n] will give a number from 0 to n, [£rand n m] will give a number from n to m.')
    async def rand(self, ctx: Context, *args):
        member: discord.Member = ctx.author
        argLen = len(args)
        
        validArgs = True
        
        for i in args:
            try:
                int(i)
            except ValueError:
                await ErrorRaiser.raiseError(ctx, member.display_name + ", one of your arguments isn't a number you fucking idiot.")
                validArgs = False
                
        if (validArgs):
            if (argLen == 0):  
                await ctx.send(str(random.random()))
            elif (argLen == 1):
                await ctx.send(str(random.randint(0, int(args[0]))))
            else:
                await ctx.send(str(random.randint(int(args[0]), int(args[1]))))