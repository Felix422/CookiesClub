import discord
from discord.ext import commands

class Tools(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.client.latency * 1000)}ms`")

    @commands.command()
    async def userinfo(self, ctx, member:discord.Member=None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(description=f"Userinfo for {member.name}", colour=discord.Colour.grey())
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Tools(client))
