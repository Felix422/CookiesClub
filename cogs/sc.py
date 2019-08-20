import discord, re, typing
from discord.ext import commands
class Showcase(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(aliases=["showcase"])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def sc(self, ctx, showcase:typing.Union[int, str]=0, mysteryshowcase=0):
        member = ctx.author
        await ctx.message.delete()
        if isinstance(showcase, int):
            if showcase < 0 or mysteryshowcase < 0:
                await ctx.send("Sc count cant be negative!")
            elif mysteryshowcase > 16 or showcase > 96:
                await ctx.send("SC count too high!", delete_after=10)
                return
            elif showcase > 50:
                await ctx.send("Showcases 50+ onward need staff permission or the nickname permission to be added as a tag.", delete_after=10)
                return
            elif showcase == 0 and mysteryshowcase == 0:
                await ctx.send("Please specify your sc item", delete_after=10)
            elif mysteryshowcase == 0:
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC#[\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    await member.edit(nick=f"{oldnick}(SC#{showcase})")
                    return
                else:
                    await member.edit(nick=f"{member.name}(SC#{showcase})")
                    return
            else:
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC#[\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    await member.edit(nick=f"{oldnick}(SC#{showcase}+{mysteryshowcase})")
                    return
                else:
                    await member.edit(nick=f"{member.name}(SC#{showcase}+{mysteryshowcase})")
                    return
        elif isinstance(showcase, str):
            if showcase == "clear":
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC#[\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    await member.edit(nick=oldnick)
                    return
                else:
                    await member.edit(nick=member.name)
                    return
                    
    @sc.error
    async def sc_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.CommandOnCooldown):
            await ctx.send("Command on cooldown")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("im not allowed to do that!", delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify your sc item", delete_after=10)
        elif isinstance(error, discord.HTTPException):
            await ctx.send("Name is longer than 32", delete_after=10)
        else:
            await ctx.send(error)

def setup(client):
    client.add_cog(Showcase(client))
