import discord, re, typing
from discord.ext import commands
from utils.checks import is_channel_allowed
class Showcase(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["showcase"])
    @commands.check(is_channel_allowed)
    @commands.cooldown(rate=2, per=10.0, type=commands.BucketType.user)
    async def sc(self, ctx, sc:typing.Union[int, str]=0, msc=0):
        member = ctx.author
        current_name = member.display_name
        if isinstance(sc, int):
            if sc < 0 or msc < 0:
                await ctx.send("Sc count cant be negative!")
            elif msc > 16 or sc > 96:
                await ctx.send("SC count too high!")
                return
            elif sc > 70:
                await ctx.send("Showcasess 70+ onward need staff permission or the nickname permission to be added as a tag.")
                return
            elif sc == 0 and msc == 0:
                e = discord.Embed(colour=discord.Color.green())
                e.set_author(name="sc")
                e.add_field(name="Usage:", value=".sc [SC] [MSC(Optional)]\n.sc clear")
                e.add_field(name="Description:", value="Sets your SC tag", inline=False)
                e.add_field(name="Aliases:", value="showcase, sc", inline=False)
                await ctx.send(embed=e)
                return
            elif msc == 0:
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[-?\d\+\s?]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    fullnick = f"{oldnick}(SC#{sc})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    return
                else:
                    fullnick = f"{member.name}(SC#{sc})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    return
            else:
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[-?\d\+\s?]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    fullnick = f"{oldnick}(SC#{sc}+{msc})"
                    if len(fullnick) > 32:
                        await ctx.send("Nickname too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    return
                else:
                    fullnick = f"{member.name}(SC#{sc}+{msc})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    return
        elif isinstance(sc, str):
            if sc == "clear":
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[-?\d\+\s?]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    await member.edit(nick=oldnick)
                    return
                else:
                    return

def setup(bot):
    bot.add_cog(Showcase(bot))
