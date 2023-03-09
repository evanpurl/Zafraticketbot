import asyncio
from discord.ext import commands
import os


class setpfp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setpfp", description="Command to set profile picture of bot.")
    @commands.has_permissions(manage_roles=True)
    async def setpfp(self, ctx) -> None:
        try:
            if ctx.message.attachments:
                for attachment in ctx.message.attachments:
                    await attachment.save("pfps/"+attachment.filename)
                    await asyncio.sleep(5) # Lets the picture be saved before changing pfp
                    with open("pfps/"+attachment.filename, 'rb') as image:
                        await self.bot.user.edit(avatar=image.read())
                        await ctx.send("Profile picture updated!")
                    os.remove("pfps/" + attachment.filename)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(setpfp(bot))
