import discord
from discord import app_commands
from discord.ext import commands

from util.dbsetget import dbsetlogchannel
from util.ticketutils import setticketdata, setticketcat


class setcmd(commands.GroupCog, name="set"):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="community-support-log",
                          description="Admin command to set the Community Support log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def csupportlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await setticketdata(guild=interaction.guild, tickettype="communitysupport", file="log", data=channel.id)
            await interaction.response.send_message(f"Your Community Support log channel has been set to {channel.mention}.",
                                                    ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="rusturned-support-log",
                          description="Admin command to set the Rusturned Support log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def rtsupportlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await setticketdata(guild=interaction.guild, tickettype="rusturnedsupport", file="log", data=channel.id)
            await interaction.response.send_message(
                f"Your Rusturned Support log channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="rp-support-log",
                          description="Admin command to set the Roleplay Support log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def rpsupportlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await setticketdata(guild=interaction.guild, tickettype="roleplaysupport", file="log", data=channel.id)
            await interaction.response.send_message(
                f"Your Roleplay Support log channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="semi-vanilla-support-log",
                          description="Admin command to set the Semi-Vanilla log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def semivanillasupportlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await setticketdata(guild=interaction.guild, tickettype="semivanillasupport", file="log", data=channel.id)
            await interaction.response.send_message(
                f"Your Semi-Vanilla Support log channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="semi-roleplay-support-log",
                          description="Admin command to set the Semi-Roleplay log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def semiroleplaysupportlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await setticketdata(guild=interaction.guild, tickettype="semiroleplaysupport", file="log", data=channel.id)
            await interaction.response.send_message(
                f"Your Semi-Roleplay Support log channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="player-report-log",
                          description="Admin command to set the Player Report log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def playerreportlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await setticketdata(guild=interaction.guild, tickettype="playerreport", file="log", data=channel.id)
            await interaction.response.send_message(
                f"Your Player Report log channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="ban-appeal-log",
                          description="Admin command to set the Ban Appeal log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def banappeallog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await setticketdata(guild=interaction.guild, tickettype="banappeal", file="log", data=channel.id)
            await interaction.response.send_message(
                f"Your Ban Appeal log channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="webstore-support-log",
                          description="Admin command to set the Webstore Support log channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def webstoresupportlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            await setticketdata(guild=interaction.guild, tickettype="webstoresupport", file="log", data=channel.id)
            await interaction.response.send_message(
                f"Your Webstore Support log channel has been set to {channel.mention}.",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @app_commands.command(name="ticket-category",
                          description="Admin command to set the ticket category.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def ticketcategory(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        try:
            await setticketcat(guild=interaction.guild, cat=category.id)
            await interaction.response.send_message(
                f"Your ticket category is set to {category.name}",
                ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)

    @csupportlog.error
    @rpsupportlog.error
    @semivanillasupportlog.error
    @playerreportlog.error
    @banappeallog.error
    @ticketcategory.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(setcmd(bot))
