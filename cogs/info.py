import discord
import itertools
import re
import platform
import os
import datetime
import typing
from uptime import _uptime_linux as linux_uptime
from subprocess import Popen, PIPE
from distro import linux_distribution as distro_info
from discord.ext import commands
from utils.checks import is_channel_allowed
from utils.pager import Pages

class HelpPaginator(Pages):
    def __init__(self, help_command, ctx, entries, *, per_page=4):
        super().__init__(ctx, entries=entries, per_page=per_page)
        self.total = len(entries)
        self.help_command = help_command
        self.prefix = help_command.clean_prefix
        self.is_bot = False

    def get_bot_page(self, page):
        cog, description, commands = self.entries[page - 1]
        self.title = f'{cog} Commands'
        self.description = description
        return commands

    def prepare_embed(self, entries, page, *, first=False):
        self.embed.clear_fields()
        self.embed.description = self.description
        self.embed.title = self.title

        self.embed.set_footer(text=f'Use "{self.prefix}help command" for more info on a command.')

        for entry in entries:
            signature = f'{entry.qualified_name} {entry.signature}'
            self.embed.add_field(name=signature, value=entry.short_doc or "No help given", inline=False)

        if self.maximum_pages:
            self.embed.set_author(name=f'Page {page}/{self.maximum_pages} ({self.total} commands)')

    async def show_bot_help(self):
        """shows how to use the bot"""

        self.embed.title = 'Using the bot'
        self.embed.description = 'Hello! Welcome to the help page.'
        self.embed.clear_fields()

        entries = (
            ('<argument>', 'This means the argument is __**required**__.'),
            ('[argument]', 'This means the argument is __**optional**__.'),
            ('[A|B]', 'This means the it can be __**either A or B**__.'),
            ('[argument...]', 'This means you can have multiple arguments.\n' \
                              'Now that you know the basics, it should be noted that...\n' \
                              '__**You do not type in the brackets!**__')
        )

        self.embed.add_field(name='How do I use this bot?', value='Reading the bot signature is pretty simple.')

        for name, value in entries:
            self.embed.add_field(name=name, value=value, inline=False)

        self.embed.set_footer(text=f'We were on page {self.current_page} before this message.')
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

class PaginatedHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category'
        })

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    async def send_bot_help(self, mapping):
        def key(c):
            return c.cog_name or '\u200bNo Category'

        bot = self.context.bot
        entries = await self.filter_commands(bot.commands, sort=True, key=key)
        nested_pages = []
        per_page = 9
        total = 0

        for cog, commands in itertools.groupby(entries, key=key):
            commands = sorted(commands, key=lambda c: c.name)
            if len(commands) == 0:
                continue

            total += len(commands)
            actual_cog = bot.get_cog(cog)
            # get the description if it exists (and the cog is valid) or return Empty embed.
            description = (actual_cog and actual_cog.description) or discord.Embed.Empty
            nested_pages.extend((cog, description, commands[i:i + per_page]) for i in range(0, len(commands), per_page))

        # a value of 1 forces the pagination session
        pages = HelpPaginator(self, self.context, nested_pages, per_page=1)

        # swap the get_page implementation to work with our nested pages.
        pages.get_page = pages.get_bot_page
        pages.is_bot = True
        pages.total = total
        await pages.paginate()

    async def send_cog_help(self, cog):
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        pages = HelpPaginator(self, self.context, entries)
        pages.title = f'{cog.qualified_name} Commands'
        pages.description = cog.description

        await pages.paginate()

    def common_command_formatting(self, page_or_embed, command):
        page_or_embed.title = self.get_command_signature(command)
        if command.description:
            page_or_embed.description = f'{command.description}\n\n{command.help}'
        else:
            page_or_embed.description = command.help or 'No help found...'

    async def send_command_help(self, command):
        # No pagination necessary for a single command.
        embed = discord.Embed(colour=discord.Colour.blurple())
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        pages = HelpPaginator(self, self.context, entries)
        self.common_command_formatting(pages, group)

        await self.context.release()
        await pages.paginate()


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = PaginatedHelpCommand()
        bot.help_command.cog = self

    def s_to_time(self, seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        return f"{days}:{hours}:{minutes}:{seconds}"

    @commands.command()
    @commands.check(is_channel_allowed)
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000)}ms`")

    @commands.command()
    @commands.check(is_channel_allowed)
    async def joinpos(self, ctx):
        await ctx.send(sorted([m for m in ctx.guild.members if not m.bot], key=lambda m: m.joined_at).index(ctx.author)+1)

    @commands.command(aliases = ["ub", "urban"])
    async def define(self, ctx, *args):
        baseurl = "https://www.urbandictionary.com/define.php?term="
        output = ""
        for word in args:
            output += word
            output += "%20"
        output = re.sub("\s","",(output.lower()))[:-3]
        await ctx.send(baseurl + output)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    @commands.check(is_channel_allowed)
    async def botinfo(self, ctx):
        bot_uptime = f"Bot uptime: {str(Popen(['ps', '-o', 'etime', '-p', str(os.getpid())], stdout=PIPE, universal_newlines=True).communicate()[0][12::]).rstrip().replace('-', ':')}"
        e = discord.Embed(title="Bot info", description="General info about the bot", color=discord.Color.blurple())
        e.add_field(name=f"Versions:",value=f"{' '.join(distro_info())}\ndiscord.py {discord.__version__}\nPython {platform.python_version()}")
        e.add_field(name="Uptime:", value=f"System uptime: {self.s_to_time(linux_uptime())}\n{bot_uptime}", inline=False)
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Info(bot))
