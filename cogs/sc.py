import discord, re, typing
from discord.ext import commands
class Showcase(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["showcase"])
    @commands.cooldown(rate=2, per=10.0, type=commands.BucketType.user)
    async def sc(self, ctx, showcase:typing.Union[int, str]=0, mysteryshowcase=0):
        member = ctx.author
        if member == ctx.guild.owner:
            await ctx.send("I cant edit the server owner!")
            return
        # await ctx.message.delete()
        if isinstance(showcase, int):
            if showcase < 0 or mysteryshowcase < 0:
                await ctx.send("Sc count cant be negative!")
            elif mysteryshowcase > 16 or showcase > 96:
                await ctx.send("SC count too high!")
                return
            elif showcase > 70:
                await ctx.send("Showcases 70+ onward need staff permission or the nickname permission to be added as a tag.")
                return
            elif showcase == 0 and mysteryshowcase == 0:
                await ctx.send("Please specify an SC item!")
            elif mysteryshowcase == 0:
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    fullnick = f"{oldnick}(SC#{showcase})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    return
                else:
                    fullnick = f"{member.name}(SC#{showcase})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    return
            else:
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    fullnick = f"{oldnick}(SC#{showcase}+{mysteryshowcase})"
                    if len(fullnick) > 32:
                        await ctx.send("Nickname too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed nickname to {fullnick}")
                    return
                else:
                    fullnick = f"{member.name}(SC#{showcase}+{mysteryshowcase})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed nickname to {fullnick}")
                    return
        elif isinstance(showcase, str):
            if showcase == "clear":
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    await member.edit(nick=oldnick)
                    return
                else:
                    await member.edit(nick=member.name)
                    return


    @sc.error
    async def sc_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("Please specify your sc item", delete_after=10)
        else:
            print(error)
            await ctx.send(error)

def setup(bot):
    bot.add_cog(Showcase(bot))
