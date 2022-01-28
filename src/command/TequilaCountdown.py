from tkinter import CURRENT
from turtle import delay
from unicodedata import name
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message
from task.CountdownTask import CountdownTask

from util.ErrorRaiser import ErrorRaiser
from util.Emojis import Emojis

class TequilaCommand(commands.Cog):
    "£tequila allows you to start the tequila countdown."

    help_brief = "This command has been created for the 2022 Tequila Battle Royale on 28th Jan 2022"
    help_description = "Follow the below usage.\n\nCommands supported:\n\n\
        • start - starts the countdown\n\
        • set - allows you to set the timer\n\nTo set, you can do something like £tequila set s 5 m 1 (set to 1 minute, 5 seconds)."
    
    SECS_MINUTE = 60
    SECS_HOUR = 60 * 60
    SECS_DAY = 60 * 60 * 24

    CURRENT_SETTING = 1200
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    def addSeconds(self, arg: str, amount: int) -> int:
        match arg:
                case "s":
                    return amount
                case "m":
                    return amount * self.SECS_MINUTE
                case "h":
                    return amount * self.SECS_HOUR
                case "d":
                    return amount * self.SECS_DAY
        
    @commands.command(name="tequila", brief=help_brief, description=help_description)
    async def tequila(self, ctx: Context, command, *timeArgs):
        try:
            countdownTask: CountdownTask = self.bot.get_cog('CountdownTask')

            if (command == 'start'):
                message: Message = await ctx.send('Countdown begins!')
                countdownTask.add_ctd(self.CURRENT_SETTING, message.channel.id, message.id, "Next tequila shot in", f"@everyone SHOTS {Emojis.PAIN}")
            elif (command == 'set'):
                if (len(timeArgs) < 1):
                    await ErrorRaiser.noArguments(ctx)
                    return
                
                # Start totalSeconds at 0
                totalSeconds: int = 0
                
                validArgs = ['s', 'm', 'h', 'd']

                for i in range(len(timeArgs)):
                    if timeArgs[i] in validArgs:
                        # For every second, minute, hour or day argument add the equivalent amount of seconds
                        totalSeconds += self.addSeconds(timeArgs[i], int(timeArgs[i + 1]))
                
                self.CURRENT_SETTING = totalSeconds
                confirmationMessage = await ctx.send("New tequila countdown parameters set.")
                await ctx.message.delete(delay=3)
                await confirmationMessage.delete(delay=3)
            else:
                await ctx.send(f"{command} is not a valid command.")
                await ctx.message.delete(delay=3)
        except:
            ErrorRaiser.catchException(ctx)
            raise
        
    
        