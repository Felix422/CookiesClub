import discord
from discord.ext import commands

class Tools(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=2, per=10.0, type=commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000)}ms`")

    # @commands.command()
    # @commands.cooldown(rate=3, per=10.0, type=commands.BucketType.user)
    # async def userinfo(self, ctx, member:discord.Member=None):
    #     if member is None:
    #         member = ctx.author
    #     embed = discord.Embed(description=f"Userinfo for {member.name}", colour=discord.Colour.grey())
    #     await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role('Staff')
    async def setnick(self, ctx, member:discord.Member, *, nick):
        await member.edit(nick=nick)
        await ctx.send(f"Set nick for {member.name} to {nick}")

    @ping.error
    async def ping_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send("Command on cooldown")

    @setnick.error
    async def setnick_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("Missing arguments")
        elif isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You dont have permission for this")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)


def setup(bot):
    bot.add_cog(Tools(bot))
