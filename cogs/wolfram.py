import discord
import asyncio

from discord.ext import commands

from config import WOLFRAM_KEY

QUERY_ERROR = commands.CommandError('Query failed. Try again later.')


class Wolfram(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['w', 'wa'])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def wolfram(self, ctx, *, query):

        params = dict(
            appid=WOLFRAM_KEY,
            i=query
        )

        async with ctx.channel.typing():
            try:
                async with self.bot.aiohttp.get('https://api.wolframalpha.com/v1/result', params=params) as resp:
                    if resp.status != 200:
                        raise QUERY_ERROR

                    res = await resp.text()
            except asyncio.TimeoutError:
                raise QUERY_ERROR

        query = query.replace('`', '\u200b`')

        embed = discord.Embed()

        embed.add_field(name='Query', value=f'```{query}```')
        embed.add_field(name='Result', value=f'```{res}```', inline=False)

        embed.set_author(name='Wolfram Alpha', icon_url='https://i.imgur.com/KFppH69.png')
        embed.set_footer(text='wolframalpha.com')

        if len(query) + len(res) > 1200:
            raise commands.CommandError('Wolfram response too long.')

        await ctx.send(embed=embed)

    @wolfram.error
    async def wolfram_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.send(f"Command on cooldown, try again in {round(error.retry_after)}s")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(F"You have to ask a question!")
            return
        else:
            await ctx.send("Query error")
            return

def setup(bot):
    bot.add_cog(Wolfram(bot))
