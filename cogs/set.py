import discord
from discord import app_commands
from discord.ext import commands

from util.dbsetget import dbsetlogchannel


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="community-support-log",
                          description="Admin command to set Community Support log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def csupportlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await dbsetlogchannel("Community Support", channel.id)
            await interaction.response.send_message(f"Your welcome channel has been set to {channel.mention}.",
                                                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @csupportlog.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(setcmd(bot))
