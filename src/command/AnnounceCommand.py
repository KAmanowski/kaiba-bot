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
                # Retreieves server and channel provided by user - this can fail
                channel = self.bot.get_channel(DynamicConfigReader.command_get_channel_id(args[0], args[1]))
                # This check checks if the channel is a TextChannel
                isinstance(channel, TextChannel)
            
                # If the third argument is a message Id, fetch the message
                message: Message = await channel.fetch_message(int(args[2]))
                # If message is found, reply to it
                await message.reply(content=args[3])
            except ValueError:
                # If the third argument was not an integer, there is no message to reply to
                # so just send the message
                await channel.send(args[2])
            except ConfigNotFoundError:
                # The user given server/channel doesn't exist
                await ctx.send("Either the server or channel you've provided is not supported.")
        else:
            await ctx.send('Not enough arguments were given. Read the guide.')