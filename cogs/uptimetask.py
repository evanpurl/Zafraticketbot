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
            guild = self.bot.get_guild(1071733132853792830)
            category = discord.utils.get(guild.categories,
                                         id=1084985136715673700)

            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                     name=f"over {len(category.channels)} ticket(s)."))
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(uptimetask(bot))
