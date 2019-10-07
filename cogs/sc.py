import re
import asyncpg
import discord
from discord.ext import commands

class SC(commands.Cog):
    """Cog class"""
    def __init__(self, bot):
        self.bot = bot
        self.regex = r"^(.*?)(\(SC\s?#\s?[-?\d\+\s?]*\)|)$"

    async def change_name(self, member, channel, showcase=0, mystery_showcase=0):
        """function for the actual name change"""
        stripped_name = re.search(self.regex, member.display_name, re.IGNORECASE).group(1)
        final_name = f'{stripped_name}(SC#{showcase}{f"+{mystery_showcase}" if mystery_showcase != 0 else ""})'
        if len(final_name) > 32:
            await channel.send("Name is too long!")
            return
        await member.edit(nick=final_name)
        await channel.send(f'Changed name to {final_name}')

    @commands.group(invoke_without_command=True, aliases=['sc'])
    async def showcase(self, ctx, showcase='0', mystery_showcase='0'):
        """adds a sc tag to a person"""
        try:
            showcase, mystery_showcase = int(showcase), int(mystery_showcase)
        except ValueError:
            await ctx.send('Invalid subcommand')
            return
        if showcase == 0 and mystery_showcase == 0:
            await ctx.send('No')
            return
        if showcase < 0 or mystery_showcase < 0:
            await ctx.send("SC count can't be negative!")
            return
        if showcase > 96 or mystery_showcase > 16:
            await ctx.send('SC count too high!')
            return
        if showcase > 70:
            sc_trusted = await self.bot.db.fetch('SELECT user_id FROM sc_trusted')
            trusted_list = [trusted_user['user_id'] for trusted_user in sc_trusted]
            if ctx.author.id in trusted_list:
                await self.change_name(ctx.author, ctx.channel, showcase, mystery_showcase)
            else:
                await ctx.send('''Showcases 70+ onward need staff permission or the nickname permission to be added as a tag.''')
        else:
            await self.change_name(ctx.author, ctx.channel, showcase, mystery_showcase)

    @showcase.command()
    async def clear(self, ctx):
        """removes the sc tag for a member"""
        if ctx.author.nick is not None:
            oldnick = re.search(self.regex, ctx.author.nick, re.IGNORECASE).group(1)
            await ctx.author.edit(nick=oldnick)

    @showcase.command()
    @commands.has_role('Staff')
    async def trust(self, ctx, member: discord.Member):
        """Removes the sc70 limit for a person"""
        try:
            await self.bot.db.fetch('INSERT INTO sc_trusted VALUES ($1)', member.id)
            await ctx.send(f"Trusted {member.mention}")
        except asyncpg.exceptions.UniqueViolationError:
            await ctx.send('User already trusted')

    @showcase.command()
    @commands.has_role('Staff')
    async def untrust(self, ctx, member: discord.Member):
        """Re-adds the sc70 limit for a person"""
        result = await self.bot.db.execute('DELETE FROM sc_trusted WHERE user_id = $1', member.id)
        if result == 'DELETE 1':
            await ctx.send(f'Untrusted {member.mention}')
        else:
            await ctx.send('User not trusted')

def setup(bot):
    """Setup function to add a cog"""
    bot.add_cog(SC(bot))
