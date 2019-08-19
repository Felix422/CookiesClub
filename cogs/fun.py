import discord, random
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["noddleslap"])
    async def noodleslap(self, ctx, member : discord.Member):

        if ctx.author == member:
            await ctx.send("You can't slap yourself!")
        else:
            await ctx.send(f"Slaps {member.mention} with noddles")

def setup(client):
    client.add_cog(Fun(client))
