import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        e.add_field(name="Acronyms", value="CC = Cupcakes\nRC = Rainbow cookies\nDC = Dark cookies\nLC = Light cookies")
        await ctx.send(embed=e)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")
        else:
            await ctx.send("Something broke, contact Felix422")

def setup(bot):
    bot.add_cog(Info(bot))
