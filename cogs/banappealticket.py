import asyncio
import datetime
import io
import chat_exporter
import discord
from discord import app_commands, ui
from discord.ext import commands
from util.dbsetget import dbgetlogchannel

timeout = 300  # seconds


# Needs "manage role" perms
# ticket-username-banappeal

def ticketembed(bot):
    embed = discord.Embed(description=f"When you are finished, click the close ticket button below. This ticket will "
                                      f"close in x minutes if no message is sent.", color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class Ticketmodal(ui.Modal, title='Ban Appeal'):
    steam64 = ui.TextInput(label='What is your Steam64 ID?', style=discord.TextStyle.short, max_length=100,
                           placeholder="(name)")
    banreason = ui.TextInput(label='For what reason were you banned?', style=discord.TextStyle.paragraph,
                             max_length=500, placeholder="(Hacking, Griefing, etc.)")
    whyunban = ui.TextInput(label='Why do you think you should be unbanned?', style=discord.TextStyle.paragraph,
                            max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
        ticketcat = discord.utils.get(interaction.guild.categories, name="Tickets")
        if ticketcat:
            ticketchan = await interaction.guild.create_text_channel(
                f"ticket-{interaction.user.name}-banappeal", category=ticketcat,
                overwrites=overwrites)
            await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                    ephemeral=True)
            await ticketchan.send(
                content=f"Welcome {interaction.user.mention}!\n\nWe will do our best to help you out.\nPlease be "
                        f"patient and wait for a staff member to respond.\n\n```Steam 64 ID:\n{self.steam64}\n\nBan "
                        f"Reason:\n{self.banreason}\n\nWhy they should be unbanned:\n{self.whyunban}```")
            await ticketchan.send(
                content=f"**Please confirm that the information above is correct.**\n"
                        f"If you do not respond in 5 minutes, this ticket will automatically close."
                        f"\n\nIf you have any extra evidence to add, please send it now.",
                embed=ticketembed(interaction.client), view=ticketbuttonpanel())

            def check(m: discord.Message):  # m = discord.Message.
                return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

            try:
                msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
            except asyncio.TimeoutError:
                lchanid = await dbgetlogchannel("Ban Appeal")
                logchannel = discord.utils.get(interaction.guild.channels,
                                               id=lchanid[0])
                if logchannel:
                    transcript = await chat_exporter.export(
                        ticketchan,
                    )
                    if transcript is None:
                        return

                    transcript_file = discord.File(
                        io.BytesIO(transcript.encode()),
                        filename=f"transcript-{ticketchan.name}.html",
                    )

                    await logchannel.send(file=transcript_file)

                await ticketchan.delete()

        else:
            ticketchan = await interaction.guild.create_text_channel(
                f"ticket-{interaction.user.name}-banappeal", overwrites=overwrites)
            await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                    ephemeral=True)
            await ticketchan.send(
                content=f"Welcome {interaction.user.mention}!\n\nWe will do our best to help you out.\nPlease be "
                        f"patient and wait for a staff member to respond.\n\n```Steam 64 ID:\n{self.steam64}\n\nBan "
                        f"Reason:\n{self.banreason}\n\nWhy they should be unbanned:\n{self.whyunban}```")
            await ticketchan.send(
                content=f"**Please confirm that the information above is correct.**\n"
                        f"If you do not respond in 5 minutes, this ticket will automatically close."
                        f"\n\nIf you have any extra evidence to add, please send it now.", embed=ticketembed(interaction.client), view=ticketbuttonpanel())

            def check(m: discord.Message):  # m = discord.Message.
                return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

            try:
                msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
            except asyncio.TimeoutError:
                lchanid = await dbgetlogchannel("Ban Appeal")
                logchannel = discord.utils.get(interaction.guild.channels,
                                               id=lchanid[0])
                if logchannel:
                    transcript = await chat_exporter.export(
                        ticketchan,
                    )
                    if transcript is None:
                        return

                    transcript_file = discord.File(
                        io.BytesIO(transcript.encode()),
                        filename=f"transcript-{ticketchan.name}.html",
                    )

                    await logchannel.send(file=transcript_file)
                await ticketchan.delete()


class ticketbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", emoji="🗑️", style=discord.ButtonStyle.red,
                       custom_id="banappeal:close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            lchanid = await dbgetlogchannel("Ban Appeal")
            logchannel = discord.utils.get(interaction.guild.channels,
                                           id=lchanid[0])
            if logchannel:
                transcript = await chat_exporter.export(
                    interaction.channel,
                )
                if transcript is None:
                    return

                transcript_file = discord.File(
                    io.BytesIO(transcript.encode()),
                    filename=f"transcript-{interaction.channel.name}.html",
                )

                await logchannel.send(file=transcript_file)
            await interaction.channel.delete()
        except Exception as e:
            print(e)

    @commands.has_permissions(manage_channels=True)
    @discord.ui.button(label="Auto-Close Ticket", emoji="⏲️", style=discord.ButtonStyle.gray,
                       custom_id="banappeal:autoclose")
    async def auto_close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.guild_permissions.manage_channels:
                await interaction.response.send_message(content="Timer started.", ephemeral=True)

                def check(m: discord.Message):  # m = discord.Message.
                    return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                try:
                    while True:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                except asyncio.TimeoutError:
                    lchanid = await dbgetlogchannel("Ban Appeal")
                    logchannel = discord.utils.get(interaction.guild.channels,
                                                   id=lchanid[0])
                    if logchannel:
                        transcript = await chat_exporter.export(
                            interaction.channel,
                        )
                        if transcript is None:
                            return

                        transcript_file = discord.File(
                            io.BytesIO(transcript.encode()),
                            filename=f"transcript-{interaction.channel.name}.html",
                        )

                        await logchannel.send(file=transcript_file)
                    await interaction.channel.delete()
                    return
            else:
                await interaction.response.send_message(content="You don't have permission to do that.", ephemeral=True)
        except Exception as e:
            print(e)


class ticketbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", emoji="📨", style=discord.ButtonStyle.blurple,
                       custom_id="banappealbutton")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            existticket = discord.utils.get(interaction.guild.channels,
                                            name=f"ticket-{interaction.user.name.lower()}-banappeal")
            if existticket:
                await interaction.response.send_message(
                    content=f"You already have an existing ticket you silly goose. {existticket.mention}",
                    ephemeral=True)
            else:
                await interaction.response.send_modal(Ticketmodal())
        except Exception as e:
            print(e)


def ticketmessageembed(bot):
    embed = discord.Embed(title="**Ban Appeals**",
                          description=f"Blah blah, this will have something in it at some point.",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class banappticketcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="ban-appeal-ticket", description="Command used by admin to create the "
                                                                "Ban Appeal ticket message.")
    async def csticket(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(embed=ticketmessageembed(self.bot), view=ticketbutton())
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(banappticketcmd(bot))
    bot.add_view(ticketbutton())  # line that inits persistent view
    bot.add_view(ticketbuttonpanel())
