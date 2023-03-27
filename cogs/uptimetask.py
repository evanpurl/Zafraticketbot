import discord
from discord.ext import commands, tasks

from util.ticketutils import getticketcat

# Needs manage messages permission

tickets = 0


class uptimetask(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        if not self.status_message.is_running():
            self.status_message.start()

    @tasks.loop(minutes=1)
    async def status_message(self):
        try:
            for guild in self.bot.guilds:
                cat = await getticketcat(guild=guild)
                category = discord.utils.get(guild.categories, id=cat)
                if category:
                    global tickets
                    tickets += len(category.channels)

            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                     name=f"{tickets} ticket(s) over {len(self.bot.guilds)} servers."))
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(uptimetask(bot))
