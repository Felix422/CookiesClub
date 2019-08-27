import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    @commands.has_role("Staff")
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount + 1)
        if amount == 1:
            await ctx.send(f"Purged {amount} message", delete_after=10)
        else:
            await ctx.send(f"Purged {amount} messages", delete_after=10)
        print(f"{ctx.author.name} purged {amount} messages in #{ctx.message.channel.name} on {ctx.message.guild.name}")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("How many messages do you want to purge?")

    @commands.command()
    @commands.has_role("Staff")
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            if (ban_entry.user.name, ban_entry.user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {ban_entry.user.name}")
                print(f"Unbanned {ban.entry.user.name}")
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("Who do you want to unban?")

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

def setup(bot):
    bot.add_cog(Moderation(bot))
