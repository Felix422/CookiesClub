import traceback, sys
from discord import Forbidden as forbidden_error
from discord.ext.commands import errors, Cog

class EH(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if any([hasattr(ctx.command, 'on_error'),
                isinstance(error, errors.CommandNotFound),
                type(error) is errors.CheckFailure]):
            return
        elif isinstance(error, errors.CommandOnCooldown):
            await ctx.send(f'Cool down! Try again in {round(error.retry_after)}s')
        elif any([isinstance(error, errors.MissingRole),
                isinstance(error, errors.NotOwner)]):
            await ctx.send('You don\'t have permission for this')
        elif isinstance(error, errors.MissingRequiredArgument):
            await ctx.send(f'Missing argument {error.param.name}')
        elif isinstance(error, errors.BadArgument):
            await ctx.send(f'Bad argument passed')
        elif isinstance(error, errors.MissingPermissions):
            perms_len = len(error.missing_perms)
            perm_word = None
            if perms_len > 1:
                perm_word = ', '.join([perm for i, perm in enumerate(error.missing_perms) if not i == perms_len - 1])
                perm_word += f' and {error.missing_perms[perms_len - 1]}'
            await ctx.send(f'You\'re missing the {perm_word or error.missing_perms[0]} permission{"s" if perms_len > 1 else ""}')
        elif isinstance(error, forbidden_error):
            await ctx.send('i don\'t have permission to do this!')
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await ctx.send('Something broke <@285738922519035904>')
            return

def setup(bot):
    bot.add_cog(EH(bot))
