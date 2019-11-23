from datetime import datetime
import discord, asyncpg
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 1):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        if amount == 1:
            await ctx.send(f"Purged {amount} message", delete_after=10)
        else:
            await ctx.send(f"Purged {amount} messages", delete_after=10)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if member is None:
            await ctx.send("Who do you want to unban?")
        banned_users = await ctx.guild.bans()
        try:
            member_name, member_discriminator = member.split("#")
        except ValueError:
            await ctx.send("invalid member")
            return
        for ban_entry in banned_users:
            if (ban_entry.user.name, ban_entry.user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f"Unbanned {ban_entry.user.name}")
                channel = discord.utils.get(ctx.guild.text_channels, name="member_logs")
                embed = discord.Embed(description=f"{ban_entry.user.name}#{ban_entry.user.discriminator} ", colour=discord.Color.green(), timestamp=datetime.utcnow())
                embed.set_thumbnail(url=ban_entry.user.avatar_url)
                embed.set_footer(text=f"User ID:{ban_entry.user.id}")
                embed.set_author(name=f"{ban_entry.user.name} got unbanned from the server", icon_url=ban_entry.user.avatar_url)
                await channel.send(embed=embed)
                return
        # await ctx.send("Member couldnt be found or isnt banned")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason, delete_message_days=7)
        await ctx.send(f"Banned {member.mention}!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx):
        await ctx.guild.leave()

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member: discord.Member, *, nick):
        if member == ctx.guild.owner:
            await ctx.send("I can't edit the server owner!")
            return
        if len(nick) > 32:
            await ctx.send("Nickname too long!")
            return
        await member.edit(nick=nick)
        await ctx.send(f"Set nick for {member.name} to {nick}")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def resetnick(self, ctx, member: discord.Member):
        await member.edit(nick=member.name)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def referralban(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Referral Banned")
        if role is None:
            await ctx.send("No role called 'Referral Banned' found")
            return
        if role in member.roles:
            await ctx.send("Member is already Referral Banned!")
            return
        await member.add_roles(role)
        await ctx.send(f"Referral Banned {member.name}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def teamshareban(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Team Share Banned")
        if role is None:
            await ctx.send("No role called 'Team Share Banned' found")
            return
        if role in member.roles:
            await ctx.send("Member is already Referral Banned!")
            return
        await member.add_roles(role)
        await ctx.send(f"Team Share Banned {member.name}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason given"):
        if member == ctx.author:
            await ctx.send("You cant warn yourself!")
            return
        if member.bot:
            await ctx.send('I cant warn bots!')
            # return
        await self.bot.db.fetch("INSERT INTO warns (user_id, guild_id, reason, epic_dude, active) VALUES ($1, $2, $3, $4, B'1')", member.id, ctx.guild.id, reason, ctx.author.id)
        await ctx.send(f"Warned {member.display_name} {f'with reason: {reason}' if reason != 'No reason given' else ''}")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(kick_members=True)
    async def warns(self, ctx, member: discord.Member):
        warns = await self.bot.db.fetch("SELECT warn_id, reason, epic_dude FROM warns WHERE user_id = $1 AND guild_id = $2 AND active = B'1'", member.id, ctx.guild.id)
        if warns == []:
            await ctx.send(f"{str(member)} has no warns!")
            return
        warn_list = []
        for warn in warns:
            warn_list.append(f"User: ({member.id}) {str(member)} Moderator: {str(ctx.guild.get_member(int(warn['epic_dude'])))}\nID:{warn['warn_id']}   {warn['reason']}")
        await ctx.send("```" + '\n'.join(warn_list) + "```")

    @warns.command(name='clear')
    @commands.has_permissions(kick_members=True)
    async def _clear(self, ctx, member: discord.Member):
        conn = await self.bot.db.acquire()
        prep = await conn.prepare("UPDATE warns SET active = B'0' WHERE user_id = $1 AND guild_id = $2 AND active = B'1'")
        await prep.fetch(member.id, ctx.guild.id)
        ret = int(prep.get_statusmsg()[::-8])
        if ret == 0:
            await ctx.send('Member doesnt have any warns!')
        else:
            await ctx.send(f'Cleared {ret} warn{"s" if ret > 1 else ""}')

    @warns.command()
    @commands.has_permissions(kick_members=True)
    async def all(self, ctx, member: discord.Member):
        conn = await self.bot.db.acquire()
        prep = await conn.prepare("SELECT warn_id, reason, epic_dude, active FROM warns WHERE user_id = $1 AND guild_id = $2")
        warns = await prep.fetch(member.id, ctx.guild.id)
        if warns == []:
            await ctx.send(f"{str(member)} has no warns!")
            return
        warn_list = []
        for warn in warns:
            warn_list.append(f"User: ({member.id}) {str(member)} Moderator: {str(ctx.guild.get_member(int(warn['epic_dude'])))}  ({'ACTIVE' if warn['active'].to_int() else 'INACTIVE'})\nID:{warn['warn_id']}   {warn['reason']}")
        await ctx.send("```" + '\n'.join(warn_list) + "```")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def allow_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        try:
            await self.bot.db.execute('insert into allowed_channels (channel_id) values ($1)', channel.id)
        except asyncpg.exceptions.UniqueViolationError:
            await ctx.send('Channel already allowed')
            return
        self.bot.allowed_channels.append(channel.id)
        await ctx.send('Allowed Channel')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def disallow_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        con = await self.bot.db.acquire()
        prep = await con.prepare('DELETE FROM allowed_channels WHERE channel_id = $1')
        await prep.fetch(channel.id)
        ret = prep.get_statusmsg()
        if ret == 'DELETE 0':
            await ctx.send('Channel is not allowed')
            return
        self.bot.allowed_channels.remove(channel.id)
        await ctx.send('Disallowed channel')

def setup(bot):
    bot.add_cog(Moderation(bot))
