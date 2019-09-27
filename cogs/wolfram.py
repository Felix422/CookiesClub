import discord
import asyncio

from discord.ext import commands

from config import WOLFRAM_KEY
class Wolfram(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['w', 'wa'])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def wolfram(self, ctx, *, query="defaultdontsearchthis"):
        if query == "defaultdontsearchthis":
            e = discord.Embed(colour=discord.Color.green())
            e.set_author(name="Wolfram")
            e.add_field(name="Usage:", value=".wolfram [question]")
            e.add_field(name="Description:", value="Queries Wolfram Alpha", inline=False)
            e.add_field(name="Aliases:", value="wolfram, w, we", inline=False)
            await ctx.send(embed=e)
            return

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
                await ctx.send("Query error")
                return

        query = query.replace('`', '\u200b`')

        embed = discord.Embed()

        embed.add_field(name='Query', value=f'```{query}```')
        embed.add_field(name='Result', value=f'```{res}```', inline=False)

        embed.set_author(name='Wolfram Alpha', icon_url='https://i.imgur.com/KFppH69.png')
        embed.set_footer(text='wolframalpha.com')

        if len(query) + len(res) > 1200:
            raise commands.CommandError('Wolfram response too long.')
        print("Queried Wolfram")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Wolfram(bot))
