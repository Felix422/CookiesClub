import discord, traceback, sys
from discord.ext import commands

class EH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if any([hasattr(ctx.command, 'on_error'),
                isinstance(error, commands.errors.CommandNotFound),
                type(error) is commands.errors.CheckFailure]):
            return
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")
        elif any([isinstance(error, commands.errors.MissingRole),
                isinstance(error, commands.errors.NotOwner)]):
            await ctx.send("You don't have permission for this")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Missing argument {error.param.name}")
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"Bad argument passed")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("i don't have permission to do this!")
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await ctx.send("Something broke <@285738922519035904>")
            return

def setup(bot):
    bot.add_cog(EH(bot))
