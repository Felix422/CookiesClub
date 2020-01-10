import discord
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

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
