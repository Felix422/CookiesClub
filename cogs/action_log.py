import discord, timeago, io
from collections import deque
from datetime import datetime
from discord.ext import commands

class Action_log(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.vclogs = deque([], 10)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is None: return
        channel = discord.utils.get(message.guild.text_channels, name="action_log")
        if channel is None: return
        if message.author.bot: return
        e = discord.Embed(color=discord.Color.red(), timestamp=datetime.utcnow(),
        description=f"**message sent by {message.author.mention} deleted in <#{message.channel.id}>**\n{message.content}",)
        e.set_author(name=message.author, icon_url=message.author.avatar_url)
        e.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")
        if message.attachments:
            attachment = message.attachments[0]
            img_bytes = io.BytesIO(await attachment.read(use_cached=True))
            file = discord.File(img_bytes, filename=attachment.filename)
            e.set_image(url=f'attachments://{attachment.filename}')
            await channel.send(embed=e, file=file)
            return
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.guild is None: return
        channel = discord.utils.get(message_before.guild.text_channels, name="action_log")
        if channel is None:
            return
        if message_before.author.bot is True:
            return
        if message_before.content == message_after.content:
            return
        e = discord.Embed(description=f"**Message edited in** <#{message_after.channel.id}> [Jump to message]({message_after.jump_url})", color=discord.Color.blurple(), timestamp=datetime.utcnow())
        try:
            e.add_field(name="Before", value=f"{message_before.content}", inline=False)
            e.add_field(name="After", value=f"{message_after.content}")
            e.set_author(name=message_before.author, icon_url=message_before.author.avatar_url)
            e.set_footer(text=f"Author: {message_after.author.id}")
            await channel.send(embed=e)
        except discord.HTTPException:
            return

    @commands.Cog.listener("on_member_update")
    async def nick_logs(self, member_before, member_after):
        if member_after.nick != member_before.nick:
            channel = discord.utils.get(member_before.guild.text_channels, name="action_log")
            if channel is None:
                return
            e = discord.Embed(description=f"**{member_after.mention} nickname changed**", color=discord.Color.blurple(), timestamp=datetime.utcnow())
            e.add_field(name="Before", value=member_before.nick if member_before.nick else member_before.name)
            e.add_field(name="After", value=member_after.nick, inline=False)
            e.set_author(name=member_before, icon_url=member_before.avatar_url)
            e.set_footer(text=f"ID: {member_after.id}")
            await channel.send(embed=e)

    @commands.Cog.listener("on_member_update")
    async def role_logs(self, member_before, member_after):
        channel = discord.utils.get(member_before.guild.text_channels, name="action_log")
        if channel is None:
            return
        if member_before.roles != member_after.roles:
            new_role = set(member_after.roles) - set(member_before.roles)
            removed_role = set(member_before.roles) - set(member_after.roles)
            if new_role != set():
                for role in new_role:
                    e = discord.Embed(description=f"Added roles to {member_before.name}", color=role.color, timestamp=datetime.utcnow())
                    e.add_field(name=f"Added roles:", value=f"`{role.name}`")
                    e.set_author(name=member_before, icon_url=member_before.avatar_url)
                    e.set_footer(text=f"ID: {member_before.id}")
                    await channel.send(embed=e)
            if removed_role != set():
                for role in removed_role:
                    e = discord.Embed(description=f"Removed roles from {member_before.name}", color=role.color, timestamp=datetime.utcnow())
                    e.add_field(name=f"Removed roles:", value=f"`{role.name}`")
                    e.set_author(name=member_before, icon_url=member_before.avatar_url)
                    e.set_footer(text=f"ID: {member_before.id}")
                    await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        channel = discord.utils.get(guild.text_channels, name="action_log")
        purge_channel = self.bot.get_channel(payload.channel_id)
        if channel is None:
            return
        e = discord.Embed(description=f"**Bulk deleted {len(payload.message_ids)} message{'s' if len(payload.message_ids) == 1 else ''} in {purge_channel.mention}**",
        color=discord.Color.blurple(), timestamp=datetime.utcnow())
        e.set_author(name=guild.name, icon_url=guild.icon_url)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        channel = discord.utils.get(ctx.guild.text_channels, name="action_log")
        if channel is None:
            return
        e = discord.Embed(description=f"Used `{ctx.command}` command in <#{ctx.channel.id}>\n{ctx.message.content}",
        color=discord.Color.blurple(), timestamp=datetime.utcnow())
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, vc_before, vc_after):
        if vc_before.channel != vc_after.channel:
            if vc_after.channel:
                time = datetime.now().strftime("%a, %I:%M%p")
                self.vclogs.append(f"{datetime.now().strftime('%a, %I:%M%p')}: {member} joined channel {vc_after.channel.name}")
            elif not vc_after.channel:
                self.vclogs.append(f"{datetime.now().strftime('%a, %I:%M%p')}: {member} left channel {vc_before.channel.name}")

    @commands.command(aliases=["vclog"])
    @commands.has_role("Staff")
    async def vclogs(self, ctx):
        await ctx.send("```" + '\n'.join(self.vclogs) + "```")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        channel = discord.utils.get(role.guild.text_channels, name="action_log")
        async for entry in channel.guild.audit_logs(limit=1):
            role_creator = entry.user
        e = discord.Embed(description=f"**New role created by {role_creator.mention}**\nName:{role.name}", color=discord.Color.green(), timestamp=datetime.utcnow())
        e.set_footer(text=f"ID: {role.id}")
        e.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        channel = discord.utils.get(role.guild.text_channels, name="action_log")
        if channel is None:
            return
        async for entry in channel.guild.audit_logs(limit=1):
            role_creator = entry.user
        e = discord.Embed(description=f"**Role deleted by {role_creator.mention}**\n{role.name}", color=discord.Color.green(), timestamp=datetime.utcnow())
        e.set_footer(text=f"ID: {role.id}")
        e.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_update(self, role_before, role_after):
        channel = discord.utils.get(role_before.guild.text_channels, name="action_log")
        if channel is None:
            return
        e = discord.Embed(title=f"Updated role {role_before.name}", color=discord.Color.blurple(), timestamp=datetime.utcnow())
        perms = set(role_after.permissions) - set(role_before.permissions)
        e.set_footer(text=f"ID: {role_before.id}")
        if role_before.permissions == role_after.permissions:
            return
        if role_before.name != role_after.name:
            e.add_field(name="Changed Name", value=f"Changed name from {role_before.name} to {role_after.name}")
        for name, value in perms:
            e.add_field(name=f"{name}", value=f"Set {name} to {value}", inline=False)
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.guild is None:
            felix = self.bot.get_user(285738922519035904)
            await felix.send(f"{message.author}: {message.content}")
        else:
            pass

def setup(bot):
    bot.add_cog(Action_log(bot))
