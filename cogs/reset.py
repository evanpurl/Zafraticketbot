import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
from util.dbsetget import dbsetlogchannel


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
        app_commands.Choice(name='Player Report', value=4),
        app_commands.Choice(name='Ban Appeal', value=5),
        app_commands.Choice(name='Webstore Support', value=6),
    ])
    async def reset(self, interaction: discord.Interaction, config: app_commands.Choice[int]) -> None:
        if config.value == 1:
            await dbsetlogchannel("Community Support", 0)
            await interaction.response.send_message(f"Community Support Log channel has been reset.", ephemeral=True)
        elif config.value == 2:
            await dbsetlogchannel("RP Support", 0)
            await interaction.response.send_message(f"RP Support Log channel has been reset.", ephemeral=True)
        elif config.value == 3:
            await dbsetlogchannel("Semi-Vanilla Support", 0)
            await interaction.response.send_message(f"Semi-Vanilla Support Log channel has been reset.", ephemeral=True)
        elif config.value == 4:
            await dbsetlogchannel("Player Report", 0)
            await interaction.response.send_message(f"Player Report Log channel has been reset.", ephemeral=True)
        elif config.value == 5:
            await dbsetlogchannel("Ban Appeal", 0)
            await interaction.response.send_message(f"Ban Appeal Log channel has been reset.", ephemeral=True)
        elif config.value == 6:
            await dbsetlogchannel("Webstore Support", 0)
            await interaction.response.send_message(f"Webstore Support Log channel has been reset.", ephemeral=True)

    @reset.error
    async def reseterror(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(content="You need admin permissions to use this command.",
                                                    ephemeral=True)
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(resetcmd(bot))
