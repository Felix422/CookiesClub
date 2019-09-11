import discord, json, traceback, sys
from discord.ext import commands


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open("warns.json", "r") as f:
                warns = json.load(f)
        except:
            print("File \"warns.json\" not found")

    @commands.command()
    @commands.has_role("Staff")
    async def warn(self, ctx, member:discord.Member=None, *, reason=None):
        if member is None:
            await ctx.send("No member specified")
            return
        if reason is None:
            await ctx.send("No reason specified")
            return
        if member == ctx.author:
            await ctx.send("You cant warn yourself!")
            return
        with open("warns.json", "r") as f:
            warns = json.load(f)
        if str(ctx.guild.id) not in warns:
            warns[str(ctx.guild.id)] = {}
        if str(member.id) not in warns[str(ctx.guild.id)]:
            warns[str(ctx.guild.id)][str(member.id)] = {"warns": []}
        warns[str(ctx.guild.id)][str(member.id)]["warns"].append(reason)
        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4, sort_keys=True)
        await ctx.send(f"Warned user {member.name} with reason {reason}")

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You don't have permission for this")
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command()
    @commands.has_role("Staff")
    async def warns(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send("No member passed")
            return
        warnlist = ""
        with open("warns.json", "r") as f:
            warns = json.load(f)
        try:
            for warn in warns[str(ctx.guild.id)][str(member.id)]["warns"]:
                warnlist = f"{warnlist} {warn}\n"
            await ctx.send(f"```{warnlist}```")
        except KeyError:
            await ctx.send("User has no warns")

    @warns.error
    async def warns_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You don't have permission for this")
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command()
    @commands.has_role("Staff")
    async def clearwarns(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send("No member passed")
            return
        with open("warns.json", "r") as f:
            warns = json.load(f)
        try:
            warns[str(ctx.guild.id)].pop(str(member.id))
            with open("warns.json", "w") as f:
                json.dump(warns, f, indent=4, sort_keys=True)
            await ctx.send(f"Cleared warns for {member.name}")
        except KeyError:
            await ctx.send("User doesnt have any warns")

    @clearwarns.error
    async def clearwarns_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You don't have permission for this")
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



def setup(bot):
    bot.add_cog(Warn(bot))
