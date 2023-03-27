import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
from util.dbsetget import dbsetlogchannel
from util.ticketutils import setticketdata


# Needs "manage role" perms

class resetcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="reset", description="Command used to reset a config option.")
    @app_commands.choices(config=[
        app_commands.Choice(name='Community Support Log', value=1),
        app_commands.Choice(name='RP Support', value=2),
        app_commands.Choice(name='Semi-Vanilla Support', value=3),
        app_commands.Choice(name='Semi-Roleplay Support', value=4),
        app_commands.Choice(name='Player Report', value=5),
        app_commands.Choice(name='Ban Appeal', value=6),
        app_commands.Choice(name='Webstore Support', value=7),
        app_commands.Choice(name='Rusturned Support', value=8),
    ])
    async def reset(self, interaction: discord.Interaction, config: app_commands.Choice[int]) -> None:
        if config.value == 1:
            await setticketdata(guild=interaction.guild, tickettype="communitysupport", file="log", data=0)
            await interaction.response.send_message(f"Community Support Log channel has been reset.", ephemeral=True)
        elif config.value == 2:
            await setticketdata(guild=interaction.guild, tickettype="roleplaysupport", file="log", data=0)
            await interaction.response.send_message(f"RP Support Log channel has been reset.", ephemeral=True)
        elif config.value == 3:
            await setticketdata(guild=interaction.guild, tickettype="semivanillasupport", file="log", data=0)
            await interaction.response.send_message(f"Semi-Vanilla Support Log channel has been reset.", ephemeral=True)
        elif config.value == 4:
            await setticketdata(guild=interaction.guild, tickettype="semiroleplaysupport", file="log", data=0)
            await interaction.response.send_message(f"Semi-Roleplay Support Log channel has been reset.", ephemeral=True)
        elif config.value == 5:
            await setticketdata(guild=interaction.guild, tickettype="playerreport", file="log", data=0)
            await interaction.response.send_message(f"Player Report Log channel has been reset.", ephemeral=True)
        elif config.value == 6:
            await setticketdata(guild=interaction.guild, tickettype="banappeal", file="log", data=0)
            await interaction.response.send_message(f"Ban Appeal Log channel has been reset.", ephemeral=True)
        elif config.value == 7:
            await setticketdata(guild=interaction.guild, tickettype="webstoresupport", file="log", data=0)
            await interaction.response.send_message(f"Webstore Support Log channel has been reset.", ephemeral=True)
        elif config.value == 8:
            await setticketdata(guild=interaction.guild, tickettype="rusturnedsupport", file="log", data=0)
            await interaction.response.send_message(f"Rusturned Support Log channel has been reset.", ephemeral=True)

    @reset.error
    async def reseterror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(content="You need admin permissions to use this command.",
                                                    ephemeral=True)
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(resetcmd(bot))
