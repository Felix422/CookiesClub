from random import randint as random
from random import choice
from discord.ext import commands
from config import COUNTER_MESSAGES

class MessageCounter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.messages_required = random(200, 400)
        self.message_counter = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return
        if message.channel.name == "general":
            self.message_counter += 1
            if self.message_counter == self.messages_required:
                await message.channel.send(choice(COUNTER_MESSAGES).format(message.author.mention))
                self.message_counter = 0
                self.messages_required = random(200, 300)

    @commands.command()
    @commands.has_role("Staff")
    async def counter(self, ctx):
        await ctx.send(f"Counter is at {self.message_counter}")


def setup(bot):
    bot.add_cog(MessageCounter(bot))
