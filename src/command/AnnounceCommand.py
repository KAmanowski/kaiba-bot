from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message
from exception.ConfigNotFound import ConfigNotFoundError

from util.DynamicConfigReader import DynamicConfigReader

class AnnounceCommand(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command()
    async def announce(self, ctx: Context, *args):
        if len(args) > 2:
            try:
                channel = self.bot.get_channel(DynamicConfigReader.command_get_channel_id(args[0], args[1]))
                isinstance(channel, TextChannel)
            
                message: Message = await channel.fetch_message(int(args[2]))
                await message.reply(content=args[3])
            except ValueError:
                await channel.send(args[2])
            except ConfigNotFoundError:
                await ctx.send("Either the server or channel you've provided is not supported.")
        else:
            await ctx.send('Not enough arguments were given. Read the guide.')