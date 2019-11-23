import discord
import textwrap
import traceback
import io
import os
import sys

from pprint import pprint
from contextlib import redirect_stdout
from tabulate import tabulate
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cleanup_code(self, content: str):
        if content.startswith('```') and content.endswith('```'):
            content = content.strip('```')
            if content.startswith('py'):
                return content.strip('py')
        return content

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
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
    async def eval(self, ctx, *, code): # stole some stuff from https://gitlab.com/nitsuga5124/nitsugabot/blob/master/cogs/debug.py
        code = self.cleanup_code(code)
        env = {
            'pprint' : pprint,
            'discord' : discord,
            'commands' : commands,
            'bot' : self.bot,
            'db' : self.bot.db,
            'ctx' : ctx

        }
        env.update(globals())
        new_forced_async_code = f'async def code():\n{textwrap.indent(code, "    ")}'
        try:
            exec(new_forced_async_code, env)
            await env['code']()
        except Exception:
            await ctx.send(f'```{traceback.format_exc()}```')

def setup(bot):
    bot.add_cog(Owner(bot))
