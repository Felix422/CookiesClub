import discord, random, traceback, sys
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["noddleslap"])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def noodleslap(self, ctx, member:discord.Member):
        invoked = "noodles" if ctx.invoked_with == "noodleslap" else "noddles"
        if member.id == 285738922519035904:
            await ctx.send(f"*Slaps {ctx.author.display_name} with {invoked}*")
            return
        elif member == self.bot.user:
            await ctx.send(":(")
            return
        elif member == ctx.author:
            await ctx.send("You can't slap yourself!")
            return
        else:
            await ctx.send(f"*Slaps {member.display_name} with {invoked}*")

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def baguette(self, ctx):
        await ctx.message.delete()
        await ctx.send("<a:nitroflex:592025304105615371>")

def setup(bot):
    bot.add_cog(Fun(bot))
