import discord, random
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["noddleslap"])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def noodleslap(self, ctx, member:discord.Member):
        if member.id == 285738922519035904:
            await ctx.send(f"*Slaps {ctx.author.mention} with noddles*")
            print(f"{ctx.author.name} tried slapping Felix!")
            return
        elif member == self.bot.user:
            await ctx.send("You cant slap me im invincible!")
            print(f"{ctx.author.name} tried slapping the bot!")
            return
        elif member == ctx.author:
            await ctx.send("You can't slap yourself!")
            print(f"{ctx.author.name} tried slapping themself")
            return
        else:
            await ctx.send(f"*Slaps {member.mention} with noddles*")
            print(f"Slapped {member.name} with noodles")

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def baguette(self, ctx):
        await ctx.send("<a:nitroflex:592025304105615371>")

    @noodleslap.error
    async def noodleslap_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")
            return
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("Bad argument")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            e = discord.Embed(colour=discord.Color.green())
            e.set_author(name="Noodleslap")
            e.add_field(name="Usage:", value=".noodleslap [user]")
            e.add_field(name="Description:", value="Slaps someone with noddles", inline=False)
            await ctx.send(embed=e)
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            return

    @baguette.error
    async def baguette_error(self, ctx, error):
         if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
             await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")

def setup(bot):
    bot.add_cog(Fun(bot))
