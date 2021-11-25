from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message
from exception.BadInputException import BadInputException
from exception.MerlinErrorException import MerlinErrorException

from task.ServerCommandBlockTask import ServerCommandBlockTask

from provider.Merlin import Merlin

class ServerCommand(commands.Cog):
  "£server lets you interact with a game server."
  
  help_brief = "Need to boot up or restart a janky valheim server? Look no further than this command."
  help_description = "Follow the below usage.\n\nCommands supported:\n\n\
    \t• start\n\
    \t• kill\n\
    \t• restart\n\n\
    Servers supported:\n\n\
    \t• valheim\n\n\
    Abuse this and you will be soft-banned."
  
  def __init__(self, bot):
      super().__init__()
      self.bot = bot
      self.lock = False
      
  async def start_server(self, ctx: Context, server: str):
    self.message = await ctx.send('Attempting to start server ' + str.upper(server) + '.')
    Merlin.server_command(server, 'start')
    await self.message.edit(content='<:coolio:802363745170358282> Server ' + str.upper(server) + ' has been started - just give it a couple of seconds to set up.')
  
  async def kill_server(self, ctx: Context, server: str):
    self.message = await ctx.send('Attempting to kill server ' + str.upper(server) + '.')
    Merlin.server_command(server, 'kill')
    await self.message.edit(content='<:pain:797622064701636648> Server ' + str.upper(server) + ' has been killed')
  
  async def restart_server(self, ctx: Context, server: str):
    self.message = await ctx.send('Attempting to restart server ' + str.upper(server) + '.')
    Merlin.server_command(server, 'restart')
    await self.message.edit(content='<:nut:802365320458403861> Server ' + str.upper(server) + ' has been restarted')
      
  @commands.command(name="server", brief=help_brief, description=help_description)
  async def server(self, ctx: Context, command, server):
    self.message: Message = None     
    bot: Bot = self.bot
    
    blocker: ServerCommandBlockTask = bot.get_cog('ServerCommandBlockTask')
    username: str = ctx.message.author.name
    
    if blocker.can_use_command(username) == False:
      await ctx.send(f"You've used too many server commands in a short time, {username}. You have been soft banned for some time.")
      return
    
    # If no server command is currently in progress
    if self.lock == False:
      try:
        # Lock server command so no one else can use it
        self.lock = True
        
        # Convert each argument to lowercase
        givenCommand = str.lower(command)
        givenServer = str.lower(server)
        # Depending on command, do one of these
        match givenCommand:
          case 'start':
            await self.start_server(ctx, givenServer)
          case 'kill':
            await self.kill_server(ctx, givenServer)
          case 'restart':
            await self.restart_server(ctx, givenServer)
          case _:
            await ctx.send(command + ' is not a valid command.')
          
          # Update the blocker counter after successful command
        blocker.update_counter(username)
      
      except BadInputException as e:
        # If Merlin can't find a server given to it by the user 
        await self.message.edit(content="Merlin says you fucked up: '" + str(e) + "'")
        await ctx.send('<:disgust2:906313723147354173>')
      except MerlinErrorException:
        # Misc Merlin error
        await self.message.edit(content='Merlin is offline/has died. Try again, maybe it might work.')
      except:
        # Something else went wrong
        await self.message.edit(content='Alright, not even I know what went wrong. No server command for you.')
      
      # Unlocks server command when everything is finished
      self.lock = False
    else:
      # If lock is active, tell the user to stop trying to break the bot
      await ctx.send("There is already a server command running, chill. Stop trying to break me - you cannot. I'll outlast you.")