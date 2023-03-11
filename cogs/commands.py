from discord.ext import commands
from util.accessutils import whohasaccess


class bcommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync", description="Command to sync slash commands")
    async def reload(self, ctx) -> None:
        tagged = ctx.message.mentions
        if tagged[0].id == self.bot.user.id:
            if await whohasaccess(ctx.message.author.id):
                print(f"Syncing commands")
                await self.bot.tree.sync()
                await ctx.send(f"Commands synced")
                print(f"Commands synced")
            else:
                await ctx.send(f"You can't run this command.")


async def setup(bot):
    await bot.add_cog(bcommands(bot))
