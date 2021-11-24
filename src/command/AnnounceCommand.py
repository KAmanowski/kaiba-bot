from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message
from exception.ConfigNotFound import ConfigNotFoundError

from util.ConfigReader import ConfigReader

class AnnounceCommand(commands.Cog):
    "£announce lets you announce something as Kaiba."
  
    help_brief = "Lets you announce something as Kaiba."
    help_description = "Can use this command in your private messages to Kaiba to not give away who used the command.\n\n\
        If you want to just send a message then just put your message in \"quotes\" as part of the messageIdOrMessage argument.\n\n\
        You can also reply to another message as Kaiba - if you have a message Id, then put the Id in as the messageIdOrMessage argument and then put your message in\
        place of the message argument.\ \n\n\
        Servers supported: kaiba\n\n\
        Channels supported: bantercave, servers, hearties, ttr (thingies to remember), valheim, dealhunters, bot, jukebox\n\n\
        Example of just a message: £announce kaiba bantercave \"Kill yourself.\"\n\n\
        Example of replying to another message: £announce kaiba bantercave <messageId> \"Kill yourself.\""
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    @commands.command(name="announce", brief=help_brief, description=help_description)
    async def announce(self, ctx: Context, server, channel, messageIdOrMessage, message=""):
        try:
            # Retrieves server and channel provided by user - this can fail
            fetchedChannel = self.bot.get_channel(ConfigReader.get_channel_id(server, channel))
            # This check checks if the channel is a TextChannel
            isinstance(fetchedChannel, TextChannel)
        
            # If the third argument is a message Id, fetch the message
            fetchedMessage: Message = await fetchedChannel.fetch_message(int(messageIdOrMessage))
            # If message is found, reply to it
            await fetchedMessage.reply(content=message)
        except ValueError:
            # If the third argument was not an integer, there is no message to reply to
            # so just send the message
            await fetchedChannel.send(messageIdOrMessage)
        except ConfigNotFoundError:
            # The user given server/channel doesn't exist
            await ctx.send("Either the server or channel you've provided is not supported.")