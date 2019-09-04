import discord
from random import randint as random
from discord.ext import commands
from config import COUNTER_MESSAGES

class MessageCounter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.messages_required = random(200, 400)
        self.message_counter = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name == "general":
            self.message_counter += 1
            if self.message_counter == self.messages_required:
                index = random.randint(0, len(COUNTER_MESSAGES) - 1)
                await message.channel.send(COUNTER_MESSAGES[index].format(message.author.mention))
                print(f"Sent counter message")
                self.message_counter = 0
                self.messages_required = random(200, 300)
                print(f"New message requirement is {self.messages_required}")

    @commands.command()
    @commands.has_role("Staff")
    async def counter(self, ctx):
        await ctx.send(f"Counter is at {self.message_counter}")

    @commands.command()
    @commands.has_role("Staff")
    async def countertest(self, ctx):
        await ctx.channel.send(COUNTER_MESSAGES[random(0, len(COUNTER_MESSAGES) - 1)].format(ctx.author.mention))


def setup(bot):
    bot.add_cog(MessageCounter(bot))
