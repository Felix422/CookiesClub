import discord, random
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["noddleslap"])
    @commands.cooldown(rate=3, per=10.0, type=commands.BucketType.user)
    async def noodleslap(self, ctx, member:discord.Member):
        if ctx.author == member:
            await ctx.send("You can't slap yourself!")
        else:
            await ctx.send(f"*Slaps {member.mention} with noddles*")

    @noodleslap.error
    async def noodleslap_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send("Command on cooldown")
            return
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("Bad argument")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("Missing required argument")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            return


def setup(bot):
    bot.add_cog(Fun(bot))
