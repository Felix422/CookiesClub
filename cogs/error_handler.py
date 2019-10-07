import discord, traceback, sys
from discord.ext import commands

class EH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")
        elif isinstance(error, commands.errors.MissingRole) or isinstance(error, commands.NotOwner):
            await ctx.send("You don't have permission for this")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"{error.param.name} is a required argument that is missing")
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"Bad argument passed")
            return
        elif isinstance(error, commands.errors.ExtensionAlreadyLoaded):
            await ctx.send("Extension already loaded")
            return
        elif isinstance(error, commands.errors.ExtensionNotFound):
            await ctx.send("Extension not found")
            return
        elif isinstance(error, discord.Forbidden):
            await ctx.send("i don't have permission to do this!")
        elif isinstance(error, commands.errors.NotOwner):
            await ctx.send("You don't have permission for this")
            return
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await ctx.send("Something broke <@285738922519035904>")
            return

def setup(bot):
    bot.add_cog(EH(bot))
