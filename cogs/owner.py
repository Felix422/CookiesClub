import discord
import textwrap
import traceback
import io
import os
import sys
from contextlib import redirect_stdout
from tabulate import tabulate
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def cleanup_code(self, content):
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    @commands.command()
    @commands.is_owner()
    async def sql(self, ctx, *, query:str):
        try:
            result = await self.bot.db.fetch(query)
        except Exception as exc:
            await ctx.send(exc)
            return
        if not len(result):
            await ctx.send("No rows returned")
            return
        table = tabulate(result, result[0].keys())
        await ctx.send('```' + table + '```')

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
    bot.add_cog(Owner(bot))
