import datetime
import io
import os
import chat_exporter
import discord
from discord import ui

from util.dbsetget import dbgetlogchannel


def ticketembed():
    embed = discord.Embed(description=f"When you are finished, click the close ticket button below.",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    return embed


def ticketmessageembed(bot, tickettype):
    embed = discord.Embed(title=f"**{tickettype} Tickets**",
                          description=f"Do you need assistance? If so, click the button below!",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


def closemessageembed(bot, user, reason):
    embed = discord.Embed(title=f"**Ticket Closed**",
                          description=f"Ticket was closed by {user.mention}",
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now())
    embed.add_field(name="Reason", value=reason)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    return embed


class closemodal(ui.Modal, title='Ticket Closure Modal'):
    def __init__(self, tickettype):
        super().__init__()
        self.ticket = tickettype

    reason = ui.TextInput(label='PLEASE GIVE A REASON FOR CLOSING THIS TICKET.', style=discord.TextStyle.paragraph,
                          max_length=600)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(content="Closing reason sent.")
            lchanid = await dbgetlogchannel(self.ticket)
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

                await logchannel.send(embed=closemessageembed(interaction.client, interaction.user, self.reason),
                                      file=transcript_file)

            await interaction.channel.delete()
        except Exception as e:
            print(e)


class autoclosemodal(ui.Modal, title='Ticket Closure Modal'):
    def __init__(self, tickettype):
        super().__init__()
        self.ticket = tickettype

    reason = ui.TextInput(label='PLEASE GIVE A REASON FOR CLOSING THIS TICKET.', style=discord.TextStyle.paragraph,
                          max_length=600)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(content="Closing reason sent.")
            lchanid = await dbgetlogchannel(self.ticket)
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

                await logchannel.send(embed=closemessageembed(interaction.client, interaction.user, self.reason),
                                      file=transcript_file)
        except Exception as e:
            print(e)


def ticketdirectories(guild, tickettype, file):
    """Used to verify ticket files for type tickettype in guild."""
    print(f"Checking ticket directory for type {tickettype} in server {guild.name}")
    dirr = f"tickets/{guild.id}/{tickettype}/{file}.txt"
    if not os.path.exists(dirr):
        print(f"{file} does not exist, creating!")
        os.makedirs(dirr)
        print(f"Created!")
    else:
        print(f"Files verified for type {tickettype} in server {guild.name}")


