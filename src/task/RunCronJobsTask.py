from discord.channel import TextChannel
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from jobs.BoysNightAnnounceJob import BoysNightAnnounceJob
from util.ConfigReader import ConfigReader
from datetime import datetime

class RunCronJobsTask(commands.Cog):
    
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.get_jobs()
        self.syncClock.start()
        
    def get_jobs(self):
      self.jobs = []
      self.jobs.append(BoysNightAnnounceJob(self.bot))
            
    @tasks.loop(minutes=1)
    async def runJobs(self):
      for job in self.jobs:
        await job.run_job()
        
    @tasks.loop(seconds=1)
    async def syncClock(self):
      current_second = int(datetime.now().strftime("%S"))
      
      if current_second == 0:
        self.syncClock.stop()
        self.runJobs.start()