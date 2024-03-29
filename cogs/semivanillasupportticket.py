import asyncio
import io
import chat_exporter
import discord
from discord import app_commands, ui
from discord.ext import commands
from util.dbsetget import dbgetlogchannel
from util.ticketutils import ticketmessageembed, ticketembed, closemodal, autoclosemodal, closemessageembed, \
    ticketdirectories, getticketdata, getticketcat

timeout = 300  # seconds

# Needs "manage role" perms
# ticket-username-semivanillasupport

tickettype = "semivanillasupport"

rolelist = ['Support Team']


class Ticketmodal(ui.Modal, title='Semi-Vanilla Support Ticket'):
    ingamename = ui.TextInput(label='WHAT IS YOUR IN-GAME NAME?', style=discord.TextStyle.short, max_length=100,
                              placeholder="(name)")
    issue = ui.TextInput(label='PLEASE EXPLAIN WHAT THIS TICKET IS ABOUT:', style=discord.TextStyle.paragraph,
                         max_length=300, placeholder="(Issue)")

    async def on_submit(self, interaction: discord.Interaction):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True)}
        cat = await getticketcat(guild=interaction.guild)
        ticketcat = discord.utils.get(interaction.guild.categories, id=cat)
        if ticketcat:
            ticketchan = await interaction.guild.create_text_channel(
                f"ticket-{interaction.user.name}-{tickettype}", category=ticketcat,
                overwrites=overwrites)

            await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                    ephemeral=True)
            await ticketchan.send(
                content=f'Welcome {interaction.user.mention}!\n\nWe will do our best to help you out.\nPlease be '
                        f'patient and wait for a staff member to respond.\n\n```json\nIn-game Name:\n"{self.ingamename}"\n\nIssue:\n"{self.issue}"```'
                        f'\n**Please confirm that the information above is correct.**'
                        f'\nIf you do not respond in 5 minutes, this ticket will automatically close.'
                        f'\n\nIf you have any extra evidence to add, please send it now.', embed=ticketembed(),
                view=ticketbuttonpanel())
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            for role in rolelist:
                await ticketchan.set_permissions(discord.utils.get(interaction.guild.roles, name=role),
                                                 overwrite=overwrite)

            def check(m: discord.Message):  # m = discord.Message.
                return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

            try:
                msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
            except asyncio.TimeoutError:
                lchanid = await getticketdata(guild=interaction.guild, tickettype=tickettype, file="log")
                logchannel = discord.utils.get(interaction.guild.channels,
                                               id=lchanid)
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

                    await logchannel.send(
                        embed=closemessageembed(interaction.client, interaction.client.user,
                                                "Ticket was closed due to inactivity."),
                        file=transcript_file)

                await ticketchan.delete()

        else:
            ticketchan = await interaction.guild.create_text_channel(
                f"ticket-{interaction.user.name}-{tickettype}", overwrites=overwrites)

            await interaction.response.send_message(content=f"Ticket created in {ticketchan.mention}!",
                                                    ephemeral=True)

            await ticketchan.send(
                content=f'Welcome {interaction.user.mention}!\n\nWe will do our best to help you out.\nPlease be '
                        f'patient and wait for a staff member to respond.\n\n```json\nIn-game Name:\n"{self.ingamename}"\n\nIssue:\n"{self.issue}"```'
                        f'\n**Please confirm that the information above is correct.**'
                        f'\nIf you do not respond in 5 minutes, this ticket will automatically close.'
                        f'\n\nIf you have any extra evidence to add, please send it now.', embed=ticketembed(),
                view=ticketbuttonpanel())
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            for role in rolelist:
                await ticketchan.set_permissions(discord.utils.get(interaction.guild.roles, name=role),
                                                 overwrite=overwrite)

            def check(m: discord.Message):  # m = discord.Message.
                return m.author.id == interaction.user.id and m.channel.id == ticketchan.id

            try:
                msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
            except asyncio.TimeoutError:
                lchanid = await getticketdata(guild=interaction.guild, tickettype=tickettype, file="log")
                logchannel = discord.utils.get(interaction.guild.channels,
                                               id=lchanid)
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

                    await logchannel.send(
                        embed=closemessageembed(interaction.client, interaction.client.user,
                                                "Ticket was closed due to inactivity."),
                        file=transcript_file)

                await ticketchan.delete()


class ticketbuttonpanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", emoji="🗑️", style=discord.ButtonStyle.red,
                       custom_id=f"{tickettype}:close", disabled=True)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if any(role.name in rolelist for role in interaction.user.roles):
                await interaction.response.send_modal(closemodal(tickettype=tickettype, file="log"))
        except Exception as e:
            print(e)

    @discord.ui.button(label="Claim Ticket", emoji="✅", style=discord.ButtonStyle.green,
                       custom_id=f"{tickettype}:claim")
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if any(role.name in rolelist for role in interaction.user.roles):
                button.disabled = True
                self.close_button.disabled = False
                self.auto_close_button.disabled = False
                await interaction.response.send_message(
                    content=f"Ticket has been claimed by {interaction.user.mention}")
                await interaction.message.edit(view=self)
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = True
                await interaction.channel.set_permissions(interaction.user, overwrite=overwrite)
            else:
                await interaction.response.send_message(content=f"You're not authorized to do that", ephemeral=True)
        except Exception as e:
            print(e)

    @discord.ui.button(label="Auto-Close Ticket", emoji="⏲️", style=discord.ButtonStyle.gray,
                       custom_id=f"{tickettype}:autoclose", disabled=True)
    async def auto_close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if any(role.name in rolelist for role in interaction.user.roles):
                await interaction.response.send_modal(autoclosemodal(tickettype=tickettype, file="log"))
                await interaction.response.send_message(content="Timer started.", ephemeral=True)

                def check(m: discord.Message):  # m = discord.Message.
                    return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                try:
                    while True:
                        msg = await interaction.client.wait_for('message', check=check, timeout=timeout)
                except asyncio.TimeoutError:
                    await interaction.channel.delete()
            else:
                await interaction.response.send_message(content="You don't have permission to do that.",
                                                        ephemeral=True)
        except Exception as e:
            print(e)


class ticketbutton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", emoji="📨", style=discord.ButtonStyle.blurple,
                       custom_id=f"{tickettype}button")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            existticket = discord.utils.get(interaction.guild.channels,
                                            name=f"ticket-{interaction.user.name.lower()}-{tickettype}")
            if existticket:
                await interaction.response.send_message(
                    content=f"You already have an existing ticket you silly goose. {existticket.mention}",
                    ephemeral=True)
            else:
                await interaction.response.send_modal(Ticketmodal())
        except Exception as e:
            print(e)


class semvticketcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            await ticketdirectories(guild=guild, tickettype=tickettype, file="log")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await ticketdirectories(guild=guild, tickettype=tickettype, file="log")

    @commands.has_permissions(manage_roles=True)
    @app_commands.command(name="semi-vanilla-support-ticket", description="Command used by admin to create the "
                                                                          "Semi-Vanilla support ticket message.")
    async def csticket(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.send_message(
                embed=ticketmessageembed(self.bot, tickettype="Semi-Vanilla Support"), view=ticketbutton())
        except Exception as e:
            print(e)

    @csticket.error
    async def onerror(self, interaction: discord.Interaction, error: app_commands.MissingPermissions):
        await interaction.response.send_message(content=error,
                                                ephemeral=True)


async def setup(bot):
    await bot.add_cog(semvticketcmd(bot))
    bot.add_view(ticketbutton())  # line that inits persistent view
    bot.add_view(ticketbuttonpanel())
