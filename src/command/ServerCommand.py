import logging
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.message import Message
from exception.BadInputException import BadInputException
from exception.MerlinErrorException import MerlinErrorException
from exception.ServerNotKillableException import ServerNotKillableException
from util.Emojis import Emojis

from task.ServerCommandBlockTask import ServerCommandBlockTask

class ServerCommand(commands.Cog):
  "£server lets you interact with a game server."
  
  help_brief = "Need to boot up or restart a janky valheim server? Look no further than this command."
  help_description = "Follow the below usage.\n\nCommands supported:\n\n\
    \t• start\n\
    \t• kill\n\
    \t• restart\n\n\
    Servers supported:\n\n\
    \t• valheim\n\n\
    \t• pz (Project Zomboid)\n\n\
    Abuse this and you will be soft-banned."
  
  def __init__(self, bot):
      super().__init__()
      self.bot = bot
      self.lock = False
      
  async def start_server(self, ctx: Context, server: str):
    self.message = await ctx.send(f'Attempting to start server {str.upper(server)}.')
    self.bot.merlin.server_command(server, 'start')
    await self.message.edit(content=f'{Emojis.COOLIO} Server {str.upper(server)} has been started - just give it a couple of seconds to set up.')
  
  async def kill_server(self, ctx: Context, server: str):
    self.message = await ctx.send(f'Attempting to kill server {str.upper(server)}.')
    self.bot.merlin.server_command(server, 'kill')
    await self.message.edit(content=f'{Emojis.PAIN} Server {str.upper(server)} has been killed')
  
  async def restart_server(self, ctx: Context, server: str):
    self.message = await ctx.send(f'Attempting to restart server {str.upper(server)}.')
    self.bot.merlin.server_command(server, 'restart')
    await self.message.edit(content=f'{Emojis.NUT} Server {str.upper(server)} has been restarted')
      
  @commands.command(name="server", brief=help_brief, description=help_description)
  @commands.cooldown(rate=1, per=15)
  async def server(self, ctx: Context, command, server):
    if self.lock == False:
      # Lock server command so no one else can use it
      self.lock = True
      self.message: Message = None     
      bot: Bot = self.bot
      
      blocker: ServerCommandBlockTask = bot.get_cog('ServerCommandBlockTask')
      username: str = ctx.message.author.name
      
      if blocker.can_use_command(username) == False:
        await ctx.send(f"You've used too many server commands in a shot time, {username}. You have been soft banned for some time.")
        return
    
    # If no server command is currently in progress
      try:
        
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
        logging.info(f"{ctx.message.author.name} tried to be naughty: " + str(e))
      except MerlinErrorException as e:
        # Misc Merlin error
        await self.message.edit(content='Merlin is offline/has died. Try again, maybe it might work.')
        logging.error("Merlin server command fail, Merlin related: " + str(e))
      except ServerNotKillableException as e:
        await self.message.edit(content='This server requires manual killing. Kaiba cannot automate this.')
      except Exception as e:
        # Something else went wrong
        await self.message.edit(content='Alright, not even I know what went wrong. No server command for you.')
        self.lock = False
        logging.error("Merlin server command fail, not Merlin related: " + str(e))
      # Unlocks server command when everything is finished
      self.lock = False
    else:
      # If lock is active, tell the user to stop trying to break the bot
      await ctx.send("There is already a server command running, chill. Stop trying to break me - you cannot. I'll outlast you.")