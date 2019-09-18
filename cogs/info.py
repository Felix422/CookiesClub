import discord
import unicodedata
import io
import textwrap
import traceback
import re
from contextlib import redirect_stdout
from pprint import pprint
from tabulate import tabulate
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cleanup_code(self, content):
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

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
        e.add_field(name="Acronyms", value="SC = Showcase\nMSC = Mystery showcase\nCC = Cupcakes\nRC = Rainbow cookies\nDC = Dark cookies\nLC = Light cookies\nIG = Intergalactic baker")
        await ctx.send(embed=e)

    @acronyms.error
    async def acronyms_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000)}ms`")
        print(f"Ping is {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def joinpos(self, ctx):
        index = list(filter(lambda m: not m.bot, sorted(ctx.guild.members, key=lambda o: o.joined_at))).index(ctx.author)+1
        await ctx.send(index)

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

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):
        """Evaluates some code."""
        env = {
            "discord": discord,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "pprint": pprint,
            "tabulate": tabulate,
        }
        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
        	exec(to_compile, env)
        except Exception as e:
        	return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
        try:
            await ctx.message.add_reaction("\u2705")
        except:
            pass
        if ret is None:
            if value:
                if len(value) > 1994:
                    fp = io.BytesIO(value.encode("utf-8"))
                    await ctx.send("Log too large...", file=discord.File(fp, "results.txt"))
        else:
            await ctx.send(f"```py\n{value}\n```")

def setup(bot):
    bot.add_cog(Info(bot))
