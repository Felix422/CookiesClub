import discord, re, typing
from discord.ext import commands
class Showcase(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sc"])
    @commands.cooldown(rate=2, per=10.0, type=commands.BucketType.user)
    async def showcase(self, ctx, showcase:typing.Union[int, str]=0, mysteryshowcase=0):
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
                e = discord.Embed(colour=discord.Color.green())
                e.set_author(name="Showcase")
                e.add_field(name="Usage:", value=".showcase [SC] [MSC(Optional)]\n.showcase clear")
                e.add_field(name="Description:", value="Sets your SC tag", inline=False)
                e.add_field(name="Aliases:", value="showcase, sc", inline=False)
                await ctx.send(embed=e)
                return
            elif mysteryshowcase == 0:
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[-?\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    fullnick = f"{oldnick}(SC#{showcase})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    print(f"Changed nickname for {member.name} to {fullnick}")
                    return
                else:
                    fullnick = f"{member.name}(SC#{showcase})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    print(f"Changed nickname for {member.name} to {fullnick}")
                    return
            else:
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[-?\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    fullnick = f"{oldnick}(SC#{showcase}+{mysteryshowcase})"
                    if len(fullnick) > 32:
                        await ctx.send("Nickname too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    print(f"Changed nickname for {member.name} to {fullnick}")
                    return
                else:
                    fullnick = f"{member.name}(SC#{showcase}+{mysteryshowcase})"
                    if len(fullnick) > 32:
                        await ctx.send("Name is too long!")
                        return
                    await member.edit(nick=fullnick)
                    await ctx.send(f"Changed your nickname to {fullnick}")
                    print(f"Changed nickname for {member.name} to {fullnick}")
                    return
        elif isinstance(showcase, str):
            if showcase == "clear":
                if member.nick is not None:
                    oldnick = re.search("^(.*?)(\(SC\s?#\s?[-?\d\+]*\)|)$", member.nick, re.IGNORECASE).group(1)
                    await member.edit(nick=oldnick)
                    return
                else:
                    return


    @showcase.error
    async def sc_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")
        else:
            print(error)
            await ctx.send(error)

def setup(bot):
    bot.add_cog(Showcase(bot))
