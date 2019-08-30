import discord
from datetime import datetime
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    @commands.has_role("Staff")
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount + 1)
        channel = discord.uils.get(ctx.guild.text_channels, name="action_log")
        if amount == 1:
            await ctx.send(f"Purged {amount} message", delete_after=10)
            e = discord.Embed(description=f"Purged {amount} message in <#{ctx.channel.id}>")
        else:
            await ctx.send(f"Purged {amount} messages", delete_after=10)
            e = discord.Embed(description=f"Purged {amount} messages in <#{ctx.channel.id}>")
        e.set_author(name=ctx.author.name, icon_url=ctx.guild.icon)
        channel.send(embed=e)
        print(f"{ctx.author.name} purged {amount} messages in #{ctx.message.channel.name} on {ctx.message.guild.name}")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("How many messages do you want to purge?")

    @commands.command()
    @commands.has_role("Staff")
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
                print(f"{ban_entry.user} got unbanned from {ctx.guild.name}")
                channel = discord.utils.get(ctx.guild.text_channels, name="member_logs")
                embed = discord.Embed(description=f"{ban_entry.user.name}#{ban_entry.user.discriminator} ", colour=discord.Color.green(), timestamp=datetime.utcnow())
                embed.set_thumbnail(url=ban_entry.user.avatar_url)
                embed.set_footer(text=f"User ID:{ban_entry.user.id}")
                embed.set_author(name=f"{ban_entry.user.name} got unbanned from the server", icon_url=ban_entry.user.avatar_url)
                await channel.send(embed=embed)
                return
        # await ctx.send("Member couldnt be found or isnt banned")

    @commands.command()
    @commands.has_role("Staff")
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention}!")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("Who do you want to ban?")

    @commands.command()
    @commands.has_role("Staff")
    async def kick(self, ctx, member:discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}")

    @kick.error
    async def Kicked_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("Who do you want to kick?")

    @commands.command()
    @commands.has_role("Staff")
    async def leave(self, ctx):
        await ctx.guild.leave()

def setup(bot):
    bot.add_cog(Moderation(bot))
