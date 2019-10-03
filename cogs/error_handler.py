import discord, traceback, sys
from discord.ext import commands

class EH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            return
        elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")
        elif isinstance(error, discord.ext.commands.errors.CommandError):
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRole) or isinstance(error, discord.ext.commands.NotOwner):
            await ctx.send("You don't have permission for this")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f"{error.param.name} is a required argument that is missing")
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("Bad argument")
            return
        elif isinstance(error, discord.ext.commands.errors.ExtensionAlreadyLoaded):
            await ctx.send("Extension already loaded")
            return
        elif isinstance(error, discord.ext.commands.errors.ExtensionNotFound):
            await ctx.send("Extension not found")
            return
        elif isinstance(error, discord.Forbidden):
            await ctx.send("i don't have permission to do this!")
        elif isinstance(error, discord.ext.commands.errors.NotOwner):
            await ctx.send("You don't have permission for this")
            return
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await ctx.send("Something broke <@285738922519035904>")
            return

def setup(bot):
    bot.add_cog(EH(bot))
