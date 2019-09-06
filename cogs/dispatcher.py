import discord
from discord.ext import commands

class Dispatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def dispatch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("invalid subcommand passed")

    @dispatch.command()
    @commands.has_role("Staff")
    async def member_remove(self, ctx):
        self.bot.dispatch("member_remove", ctx.author)

    @dispatch.command()
    @commands.has_role("Staff")
    async def member_join(self, ctx):
        self.bot.dispatch("member_join", ctx.author)

def setup(bot):
    bot.add_cog(Dispatcher(bot))
