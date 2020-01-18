import re
from discord import Member
from discord.utils import get
from asyncpg.exceptions import UniqueViolationError
from discord.ext.commands import Cog, command, check, group, has_role
from utils.checks import is_channel_allowed

class SC(Cog):
    """Showcase name tags"""
    def __init__(self, bot):
        self.bot = bot
        self.regex = re.compile(r'^(?P<name>.*?)(?P<tag>\(SC\s?#\s?[-?\d\+\s?]*\)|)$',
                                re.IGNORECASE)

    @property
    def db(self):
        return self.bot.db

    async def change_name(self, member, channel, showcase=0, mystery_showcase=0):
        '''function for the actual name change'''
        stripped_name = self.regex.search(member.display_name).group('name')
        msc_tag = f'+{mystery_showcase}' if mystery_showcase != 0 else ''
        full_tag = f'(SC#{showcase}{msc_tag})'
        final_name = f'{stripped_name}{full_tag}'
        if len(final_name) > 32:
            await channel.send('Name is too long!')
            return
        await member.edit(nick=final_name)
        await channel.send(f'Changed name to {final_name}')

    @group(invoke_without_command=True, aliases=['sc'])
    @check(is_channel_allowed)
    async def showcase(self, ctx, showcase='0', mystery_showcase='0'):
        '''adds a sc tag to a person'''
        try:
            showcase, mystery_showcase = int(showcase), int(mystery_showcase)
        except ValueError:
            await ctx.send('Invalid subcommand')
            return
        if showcase == 0 and mystery_showcase == 0:
            await ctx.send('No')
            return
        if showcase < 0 or mystery_showcase < 0:
            await ctx.send('SC count can\'t be negative!')
            return
        if showcase > 96 or mystery_showcase > 16:
            await ctx.send('SC count too high!')
            return
        if showcase > 70:
            sc_trusted = await self.db.fetch('SELECT user_id FROM sc_trusted')
            trusted_list = [trusted_user['user_id'] for trusted_user in sc_trusted]
            allowed = any([ctx.author.id in trusted_list,
                get(ctx.guild.roles, name='Staff') in ctx.author.roles,
                ctx.author.guild_permissions.manage_nicknames,
                ctx.author.guild_permissions.change_nickname,
                ctx.author.guild_permissions.administrator])
            if allowed:
                await self.change_name(ctx.author, ctx.channel, showcase, mystery_showcase)
            else:
                await ctx.send(('Showcases 70 and onward need staff permission'
                            ' or being on the trusted list to be used as a tag'))
        else:
            await self.change_name(ctx.author, ctx.channel, showcase, mystery_showcase)

    @showcase.command()
    @check(is_channel_allowed)
    async def clear(self, ctx):
        '''removes the sc tag for a member'''
        if ctx.author.nick is not None:
            oldnick = re.search(self.regex, ctx.author.nick, re.IGNORECASE).group(1)
            await ctx.author.edit(nick=oldnick)

    @showcase.command()
    @has_role('Staff')
    async def trust(self, ctx, member: Member):
        '''Removes the sc70 limit for a person'''
        try:
            await self.db.fetch('INSERT INTO sc_trusted VALUES ($1)', member.id)
            await ctx.send(f'Trusted {member.mention}')
        except UniqueViolationError:
            await ctx.send('User already trusted')

    @showcase.command()
    @has_role('Staff')
    async def untrust(self, ctx, member: Member):
        '''Re-adds the sc70 limit for a person'''
        result = await self.db.execute('DELETE FROM sc_trusted WHERE user_id = $1', member.id)
        if result == 'DELETE 1':
            await ctx.send(f'Untrusted {member.mention}')
        else:
            await ctx.send('User not trusted')

    # @showcase.command()
    # async def update(self, ctx):
        # name = self.regex.search(ctx.author.display_name).group('tag')


def setup(bot):
    '''Setup function to add a cog'''
    bot.add_cog(SC(bot))
