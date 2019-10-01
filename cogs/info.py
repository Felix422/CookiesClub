import discord
import unicodedata
import re
import platform
import os
import datetime
import typing
from uptime import _uptime_linux as linux_uptime
from subprocess import Popen, PIPE
from distro import linux_distribution as distro_info
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def s_to_time(self, seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        return f"{days}-{hours}:{minutes}:{seconds}"

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def help(self, ctx, command=None):
        e = discord.Embed(colour=discord.Color.green())
        if command is None:
            e.add_field(name="Commands:",value=".showcase\n.noodleslap\n.wolfram\n.ping\n.acronyms")
            await ctx.send(embed=e)
            return
        elif command.lower() == "showcase" or command.lower() == "sc":
            e.set_author(name="Showcase")
            e.add_field(name="Usage:", value=".showcase [SC] [MSC(Optional)]\n.showcase clear")
            e.add_field(name="Description:", value="Sets your SC tag", inline=False)
            e.add_field(name="Aliases:", value="showcase, sc", inline=False)
            await ctx.send(embed=e)
            return
        elif command.lower() == "noodleslap":
            e.set_author(name="Noodleslap")
            e.add_field(name="Usage:", value=".noodleslap [user]")
            e.add_field(name="Description:", value="Slaps someone with noddles", inline=False)
            await ctx.send(embed=e)
            return
        elif command.lower() == "wolfram" or command.lower() == "w":
            e.set_author(name="Wolfram")
            e.add_field(name="Usage:", value=".wolfram [question]")
            e.add_field(name="Description:", value="Queries Wolfram Alpha", inline=False)
            e.add_field(name="Aliases:", value="wolfram, w, we", inline=False)
            await ctx.send(embed=e)
            return
        elif command.lower() == "ping":
            e.set_author(name="Ping")
            e.add_field(name="Usage:", value=".ping")
            e.add_field(name="Description:", value="Shows the bots latency", inline=False)
            await ctx.send(embed=e)
            return
        elif command.lower() == "acronyms":
            e.set_author(name="Acronyms")
            e.add_field(name="Usage:", value=".acronyms")
            e.add_field(name="Description:", value="Lists the most used acronyms", inline=False)
            await ctx.send(embed=e)
        else:
            await ctx.send(f"Command `{command}` not found")

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def acronyms(self, ctx):
        e = discord.Embed(color=discord.Color.green())
        e.add_field(name="Acronyms", value="""SC = Showcase\nMSC = Mystery showcase\nCC = Cupcakes\nRC = Rainbow cookies\nDC = Dark cookies\nLC = Light cookies\nIG = Intergalactic baker""")
        await ctx.send(embed=e)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000)}ms`")
        print(f"Ping is {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def joinpos(self, ctx):
        await ctx.send(list(filter(lambda m: not m.bot, sorted(ctx.guild.members, key=lambda o: o.joined_at))).index(ctx.author)+1)

    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        def to_string(c):
            digit = f"{ord(c):x}"
            name = unicodedata.name(c, "Name not found.")
            return f"`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>"
        msg = "\n".join(map(to_string, characters))
        if len(msg) > 2000:
            return await ctx.send("Output too long to display.")
        await ctx.send(msg)

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
    async def botinfo(self, ctx):
        bot_uptime = f"Bot uptime: {str(Popen(['ps', '-o', 'etime', '-p', str(os.getpid())], stdout=PIPE, universal_newlines=True).communicate()[0][12::]).rstrip()}"
        e = discord.Embed(title="Bot info", description="General info about the bot", color=discord.Color.blurple())
        e.add_field(name=f"Versions:",value=f"{' '.join(distro_info())}\ndiscord.py {discord.__version__}\nPython {platform.python_version()}")
        e.add_field(name="Uptime:", value=f"System uptime: {self.s_to_time(linux_uptime())}\n{bot_uptime}", inline=False)
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Info(bot))
