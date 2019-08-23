import discord
from discord.ext import commands
from datetime import datetime

class Tools(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=2, per=10.0, type=commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000)}ms`", delete_after=10)

    # @commands.command()
    # @commands.cooldown(rate=3, per=10.0, type=commands.BucketType.user)
    # async def userinfo(self, ctx, member:discord.Member=None):
    #     if member is None:
    #         member = ctx.author
    #     embed = discord.Embed(description=f"Userinfo for {member.name}", colour=discord.Colour.grey())
    #     await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def help(self, ctx, command=None):
        e = discord.Embed(colour=discord.Color.green())
        if command is None:
            e.add_field(name="Commands:",value=".showcase\n.noodleslap\n.wolfram\n.ping")
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
            e.set_author(name="Noodlesllap")
            e.add_field(name="Usage:", value=".noodleslap [user]")
            e.add_field(name="Description:", value="Slaps someone with noddles", inline=False)
            await ctx.send(embed=e)
            return
        elif command.lower() == "wolfram" or command.lower() == "w":
            e.set_author(name="Wolfram")
            e.add_field(name="Usage:", value=".wolfram [question]")
            e.add_field(name="Description:", value="Queries Wolfram alpha", inline=False)
            e.add_field(name="Aliases:", value="wolfram, w, we", inline=False)
            await ctx.send(embed=e)
            return
        elif command.lower() == "ping":
            e.set_author(name="Ping")
            e.add_field(name="Usage:", value=".ping")
            e.add_field(name="Description:", value="Shows the bots latency", inline=False)
            await ctx.send(embed=e)
            return

    @commands.command()
    @commands.has_role('Staff')
    async def setnick(self, ctx, member:discord.Member, *, nick):
        if member == ctx.guild.owner:
            await ctx.send("I can't edit the server owner!")
            return
        if len(nick) > 32:
            await ctx.send("Nickname too long!")
            return
        await member.edit(nick=nick)
        await ctx.send(f"Set nick for {member.name} to {nick}")

    @commands.command()
    @commands.has_role('Staff')
    async def resetnick(self, ctx, member:discord.Member):
        if member == ctx.guild.owner:
            await ctx.send("I can't edit the server owner!")
            return
        await member.edit(nick=member.name)

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
            await ctx.send("You don't have permission for this")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)


def setup(bot):
    bot.add_cog(Tools(bot))
