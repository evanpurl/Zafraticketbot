import discord
from discord import app_commands
from discord.ext import commands


class creatorcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="creator", description="Command to tell you who made me!")
    async def creator(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(
                content=f"""{interaction.user.mention}, {self.bot.user.name} was created by Purls, and is hosted by 
                Wyvern server hosting. Want your own bot? Head to https://discord.gg/Wdunj8yCxZ""",
                ephemeral=True)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(creatorcmd(bot))