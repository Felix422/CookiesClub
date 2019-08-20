import discord, random
from discord.ext import commands
from config import *

class MessageCounter(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.message_counter = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name == "general":
            self.client.message_counter += 1
            if self.client.message_counter == 300:
                index = random.randint(0, len(dictionary) - 1)
                await message.channel.send(index + 1)
                await message.channel.send(dictionary[index].format(message.author.mention))
                self.client.message_counter = 0

    @commands.command
    async def counter(self, ctx):
        await ctx.send(f"Counter is at {self.client.message_counter}")


def setup(client):
    client.add_cog(MessageCounter(client))
