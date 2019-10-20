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
    async def eval(self, ctx, *, code):
        if 'import os' in code or 'import sys' in code or 'from config import BOT_TOKEN' in code:
            return
        code = code.strip('` ')
        env = {
            'discord' : discord,
            'commands' : commands,
            'bot' : self.bot,
            'db' : self.bot.db,
            'ctx' : ctx

        }
        env.update(globals())
        new_forced_async_code = f'async def code():\n{textwrap.indent(code, "    ")}'
        exec(new_forced_async_code, env)
        code = env['code']
        try:
            await code()
        except Exception:
            await ctx.send(f'```{traceback.format_exc()}```')

def setup(bot):
    bot.add_cog(Owner(bot))
