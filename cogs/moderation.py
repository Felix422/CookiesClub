import discord, traceback, sys, json
from datetime import datetime
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        try:
            with open("warns.json", "r") as f:
                warns = json.load(f)
        except:
            print("File \"warns.json\" not found")

    @commands.command(aliases=["purge"])
    @commands.has_role("Staff")
    async def clear(self, ctx, amount : int = 1):
        await ctx.channel.purge(limit=amount + 1)
        if amount == 1:
            await ctx.send(f"Purged {amount} message", delete_after=10)
        else:
            await ctx.send(f"Purged {amount} messages", delete_after=10)

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

    @commands.command()
    @commands.has_role("Staff")
    async def setnick(self, ctx, member:discord.Member, *, nick):
        if member == ctx.guild.owner:
            await ctx.send("I can't edit the server owner!")
            return
            if len(nick) > 32:
                await ctx.send("Nickname too long!")
                return
                await member.edit(nick=nick)
                await ctx.send(f"Set nick for {member.name} to {nick}")

    @setnick.error
    async def setnick_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("Missing arguments")
        elif isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You don't have permission for this")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)

    @commands.command()
    @commands.has_role("Staff")
    async def resetnick(self, ctx, member:discord.Member):
        if member == ctx.guild.owner:
            await ctx.send("I can't edit the server owner!")
            return
        await member.edit(nick=member.name)

    @resetnick.error
    async def resetnick_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You don't have permission for this")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)

    @commands.command()
    async def referralban(self, ctx, member:discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Referral Banned")
        if role == None:
            await ctx.send("No role called \"Referral Banned\" found")
            return
        if role in member.roles:
            await ctx.send("Member is already Referral Banned!")
            return
        await member.add_roles(role)
        await ctx.send(f"Referral Banned {member.name}")

    @referralban.error
    async def referralban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("Member not found")
        elif isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You dont have permissions for this!")
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command()
    @commands.has_role("Staff")
    async def teamshareban(self, ctx, member:discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Team Share Banned")
        if role == None:
            await ctx.send("No role called \"Team Share Banned\" found")
            return
        if role in member.roles:
            await ctx.send("Member is already Referral Banned!")
            return
        await member.add_roles(role)
        await ctx.send(f"Team Share Banned {member.name}")

    @teamshareban.error
    async def teamshareban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("Member not found")
        elif isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You dont have permissions for this!")
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

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
    bot.add_cog(Moderation(bot))
