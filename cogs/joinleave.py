import discord, timeago
from datetime import datetime
from discord.ext import commands

class JoinLeave(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} joined the server")
        channelname = self.client.get_channel(558056889938739201)
        embed = discord.Embed(description=f"{member.mention} {member.name}#{member.discriminator} ", colour=discord.Color.green(), timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Account age", value=f"Created {timeago.format(member.created_at, datetime.now())}")
        embed.set_footer(text=f"User ID:{member.id}")
        embed.set_author(name=f"{member.name} has joined the server", icon_url=member.avatar_url)
        await channelname.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} left the server")
        channelname = self.client.get_channel(558056889938739201)
        embed = discord.Embed(description=f"{member.mention} {member.name}#{member.discriminator} ", colour=discord.Color.red(), timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"User ID:{member.id}")
        embed.set_author(name=f"{member.name} left the server", icon_url=member.avatar_url)
        await channelname.send(embed=embed)

def setup(client):
    client.add_cog(JoinLeave(client))
