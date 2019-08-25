import discord, timeago
from datetime import datetime
from discord.ext import commands

class JoinLeave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} joined {member.guild.name}")
        channel = discord.utils.get(member.guild.text_channels, name="member_logs")
        embed = discord.Embed(description=f"{member.mention} {member.name}#{member.discriminator} ", colour=discord.Color.green(), timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Account age", value=f"Created {timeago.format(member.created_at, datetime.now())}")
        embed.set_footer(text=f"User ID:{member.id}")
        embed.set_author(name=f"{member.name} has joined the server", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} left {member.guild.name}")
        channel = discord.utils.get(member.guild.text_channels, name="member_logs")
        embed = discord.Embed(description=f"{member.mention} {member.name}#{member.discriminator} ", colour=discord.Color.red(), timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"User ID:{member.id}")
        embed.set_author(name=f"{member.name} left the server", icon_url=member.avatar_url)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(JoinLeave(bot))
