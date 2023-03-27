import discord
from discord import app_commands
from discord.ext import commands

from util.dbsetget import dbsetlogchannel
from util.ticketutils import setticketdata, deleteticketdirectories


class botleft(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await deleteticketdirectories(guild)


async def setup(bot):
    await bot.add_cog(botleft(bot))
