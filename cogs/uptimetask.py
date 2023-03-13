import time, datetime
import discord
from discord.ext import commands, tasks

# Needs manage messages permission

starttime = 0.0
class uptimetask(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        global starttime
        starttime = time.time()  # Get time in seconds at start
        if not self.status_message.is_running():
            self.status_message.start()

    @tasks.loop(minutes=1)
    async def status_message(self):
        try:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                   name=f"/creator \n {datetime.timedelta(seconds=round(time.time() - starttime))}"))
        except Exception as e:
            print(e)



async def setup(bot):
    await bot.add_cog(uptimetask(bot))