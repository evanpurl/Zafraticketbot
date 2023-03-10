import datetime

import discord
from discord import app_commands, ui
from discord.ext import commands


# Needs "manage role" perms
# ticket-username-communitysupport

class Ticketmodal(ui.Modal, title='Community Support Ticket'):
    issue = ui.TextInput(label='Please describe your issue', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
        existticket = discord.utils.get(interaction.guild.channels,
                                        name=f"ticket-{interaction.user.name.lower()}-communitysupport")
        if existticket:
            await interaction.response.send_message(
                content=f"You already have an existing ticket you silly goose. {existticket.mention}", ephemeral=True)
        else:
            ticketcat = discord.utils.get(interaction.guild.categories, name="Tickets")
            if ticketcat:
                ticketchan = await interaction.guild.create_text_channel(
                    f"ticket-{interaction.user.name}-communitysupport", category=ticketcat,
                    overwrites=overwrites)
                await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                        ephemeral=True)
                await ticketchan.send(
                    content=f"User {interaction.user.mention} created a ticket for reason: {self.issue}")

            else:
                ticketchan = await interaction.guild.create_text_channel(
                    f"ticket-{interaction.user.name}-communitysupport", overwrites=overwrites)
                await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                        ephemeral=True)
                await ticketchan.send(
                    content=f"User {interaction.user.mention} created a ticket for reason: {self.issue}")


class ticketbutton(discord.ui.View):

    @discord.ui.button(label="📨 Create Ticket", style=discord.ButtonStyle.blurple)
    async def gray_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(Ticketmodal())


def ticketmessageembed(bot):
    embed = discord.Embed(title="**Community Support Tickets**",
                          description=f"Blah blah, this will have something in it at some point.",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class ticketcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="communitysupportticket", description="Command used by admin to create the community "
                                                                     "support ticket message.")
    async def csticket(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=ticketmessageembed(self.bot), view=ticketbutton())
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(ticketcmd(bot))
