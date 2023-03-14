import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import os


class setpfp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setpfp", description="Command to set profile picture of bot.")
    @commands.has_permissions(manage_roles=True)
    async def setpfp(self, interaction: discord.Interaction, pfp: discord.Attachment) -> None:
        fnames = (".png", ".jpg", ".jpeg")
        try:
            if pfp.filename.endswith(fnames):
                if not os.path.exists("pfps/"):
                    os.mkdir("pfps/")
                await pfp.save("pfps/" + pfp.filename)
                await interaction.response.defer(ephemeral=True)
                await asyncio.sleep(5)  # Lets the picture be saved before changing pfp
                with open("pfps/" + pfp.filename, 'rb') as image:
                    await self.bot.user.edit(avatar=image.read())
                    await interaction.followup.send(content="Profile picture updated!", ephemeral=True)
                os.remove("pfps/" + pfp.filename)
            else:
                await interaction.response.send_message(content="Cannot process unknown file.", ephemeral=True)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(setpfp(bot))
