from discord.channel import TextChannel
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
import time
import datetime
import asyncio
import _thread

from discord.message import Message
from task.CountdownTask import CountdownTask

from util.ErrorRaiser import ErrorRaiser

class CountdownCommand(commands.Cog):
    
    SECS_MINUTE = 60
    SECS_HOUR = 60 * 60
    SECS_DAY = 60 * 60 * 24
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    def addSeconds(arg: str, amount: int) -> int:
        match arg:
                case "s":
                    return amount
                case "m":
                    return amount * CountdownCommand.SECS_MINUTE
                case "h":
                    return amount * CountdownCommand.SECS_HOUR
                case "d":
                    return amount * CountdownCommand.SECS_DAY
        
    @commands.command()
    async def ctd(self, ctx: Context, *args):
        try:
            if (len(args) < 1):
                await ErrorRaiser.noArguments(ctx)
                return
            
            # Start totalSeconds at 0
            totalSeconds: int = 0
            
            validArgs = ['s', 'm', 'h', 'd']
            
            for i in range(len(args)):
                if args[i] in validArgs:
                    # For every second, minute, hour or day argument add the equivalent amount of seconds
                    totalSeconds += CountdownCommand.addSeconds(args[i], int(args[i + 1]))
            
            countdownTask: CountdownTask = self.bot.get_cog('CountdownTask')
            
            message: Message = await ctx.send('Countdown begins!')
            countdownTask.add_ctd(totalSeconds, message.channel.id, message.id)
        except:
            ErrorRaiser.catchException(ctx)
            raise
        
    
        