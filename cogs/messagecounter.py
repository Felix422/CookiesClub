import discord, random
from discord.ext import commands
from config import *

class MessageCounter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.message_counter = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name == "general":
            self.bot.message_counter += 1
            if self.bot.message_counter == 300:
                index = random.randint(0, len(dictionary) - 1)
                await message.channel.send(index + 1)
                await message.channel.send(dictionary[index].format(message.author.mention))
                self.bot.message_counter = 0

    @commands.command
    async def counter(self, ctx):
        await ctx.send(f"Counter is at {self.bot.message_counter}")


def setup(bot):
    bot.add_cog(MessageCounter(bot))
