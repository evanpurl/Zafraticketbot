import datetime
import io
import os
import chat_exporter
import discord
from discord import ui


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
    def __init__(self, tickettype, file):
        super().__init__()
        self.ticket = tickettype
        self.file = file

    reason = ui.TextInput(label='PLEASE GIVE A REASON FOR CLOSING THIS TICKET.', style=discord.TextStyle.paragraph,
                          max_length=600)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(content="Closing reason sent.")
            lchanid = await getticketdata(guild=interaction.guild, tickettype=self.ticket, file=self.file)
            logchannel = discord.utils.get(interaction.guild.channels,
                                           id=lchanid)
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
    def __init__(self, tickettype, file):
        super().__init__()
        self.ticket = tickettype
        self.file = file

    reason = ui.TextInput(label='PLEASE GIVE A REASON FOR CLOSING THIS TICKET.', style=discord.TextStyle.paragraph,
                          max_length=600)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(content="Closing reason sent.")
            lchanid = await getticketdata(guild=interaction.guild, tickettype=self.ticket, file=self.file)
            logchannel = discord.utils.get(interaction.guild.channels,
                                           id=lchanid)
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


async def ticketdirectories(guild, tickettype, file):
    """Used to verify ticket files for type tickettype in guild."""
    print(f"Checking ticket directory for type {tickettype} in server {guild.name}")
    dirr = f"tickets/{guild.id}/{tickettype}/{file}.txt"
    if not os.path.exists(dirr):
        print(f"{file} does not exist, creating!")
        os.makedirs(os.path.dirname(dirr))
        with open(dirr, "w") as f:
            f.write(f"0")
        print(f"Created!")
    else:
        print(f"Files verified for type {tickettype} in server {guild.name}")


async def deleteticketdirectories(guild):
    dirr = f"tickets/{guild.id}"
    if os.path.exists(dirr):
        print(f"Deleting server ticket folders for {guild.name}")
        os.remove(dirr)
        print(f"Deleted")


async def getticketdata(guild, tickettype, file):
    dirr = f"tickets/{guild.id}/{tickettype}/{file}.txt"
    if os.path.exists(dirr):
        with open(dirr, "r") as f:
            data = f.readline()
        return int(data)
    else:
        return 0


async def setticketdata(guild, tickettype, file, data):
    dirr = f"tickets/{guild.id}/{tickettype}/{file}.txt"
    if os.path.exists(dirr):
        with open(dirr, "w") as f:
            f.write(str(data))
        return 1
    else:
        return 0


async def setticketcat(guild, cat):
    dirr = f"config/{guild.id}/ticketcategory.txt"
    if os.path.exists(dirr):
        with open(dirr, "w") as f:
            f.write(str(cat))
        return 1
    else:
        os.makedirs(os.path.dirname(dirr))
        with open(dirr, "w") as f:
            f.write(str(cat))


async def getticketcat(guild):
    dirr = f"config/{guild.id}/ticketcategory.txt"
    if os.path.exists(dirr):
        with open(dirr, "r") as f:
            data = f.readline()
        return int(data)
    else:
        return 0
