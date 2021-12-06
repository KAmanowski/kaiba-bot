from discord.ext import commands, tasks

class ServerCommandBlockTask(commands.Cog):
    
    MAX_COMMANDS = 500
    
    task_name = 'remove_server_command_blocks'
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.naughties: dict = {}
        self.lastNaughties: dict = {}
        self.remove_server_command_blocks.start()
        
    def update_counter(self, userId: str, amount=1):
        if userId in self.naughties:
            self.naughties[userId] = self.naughties[userId] + amount
        else:
            self.naughties[userId] = amount
        
    def can_use_command(self, userId: str) -> bool:
        if userId in self.naughties:
            if self.naughties[userId] >= self.MAX_COMMANDS:
                return False
            else:
                return True
        else:
            return True
        
    @tasks.loop(minutes=15)
    async def remove_server_command_blocks(self):
        newNaughties: dict = {}
        for naughtyUser in self.lastNaughties:
            # If user got soft-banned last refresh, give them less commands
            if naughtyUser in self.naughties and self.naughties[naughtyUser] >= self.MAX_COMMANDS:
                newNaughties[naughtyUser] = self.MAX_COMMANDS - 2

        self.lastNaughties = self.naughties
        self.naughties = newNaughties
        
            