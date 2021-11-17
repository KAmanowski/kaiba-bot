from discord.ext import commands, tasks
from discord.ext.commands.context import Context
import time
import datetime
import asyncio
import _thread

from discord.message import Message

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
        
    def formatSeconds(seconds: int) -> str:
        if seconds is not None:
            d = seconds // (3600 * 24)
            h = seconds // 3600 % 24
            m = seconds % 3600 // 60
            s = seconds % 3600 % 60
            if d > 0:
                return '{:02d}D {:02d}H {:02d}m {:02d}s'.format(d, h, m, s)
            elif h > 0:
                return '{:02d}H {:02d}m {:02d}s'.format(h, m, s)
            elif m > 0:
                return '{:02d}m {:02d}s'.format(m, s)
            elif s > 0:
                return '{:02d}s'.format(s)
        return "Time's up you fucks."
          
    @tasks.loop(seconds=1.0)
    async def countDown(ctx: Context, seconds: int, printMessage: bool = True):
        message = ""
        if (printMessage):
            message: Message = await ctx.send(CountdownCommand.formatSeconds(seconds))
        
        while (seconds >= 0):
            if (printMessage):
                await message.edit(content = CountdownCommand.formatSeconds(seconds))
                
            await asyncio.sleep(1)
            seconds = seconds - 1
        
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
            
            asyncio.create_task(CountdownCommand.countDown(ctx, totalSeconds))
        except:
            ErrorRaiser.catchException(ctx)
            raise
        
    
        