import discord
from discord.ext import commands
from config import WOLFRAM_KEY

class Wolfram(commands.Cog):

    def __init__(self, client):
        self.client = client
        query_error = commands.CommandError('Query failed. Try again later.')

#     @commands.command(aliases=['w', 'wa'])
# 	@commands.bot_has_permissions(embed_links=True)
# 	@commands.cooldown(rate=3, per=10.0, type=commands.BucketType.user)
# 	async def wolfram(self, ctx, *, query):
#
# 		params = {
# 			'appid': WOLFRAM_KEY,
# 			'i': query
# 		}
#
# 		async with ctx.channel.typing():
# 			try:
# 				async with self.bot.aiohttp.get('https://api.wolframalpha.com/v1/result', params=params) as resp:
# 					if resp.status != 200:
# 						raise self.query_error
#
# 					res = await resp.text()
# 			except asyncio.TimeoutError:
# 				raise self.query_error
#
# 		query = query.replace('`', '\u200b`')
#
# 		embed = discord.Embed()
#
# 		embed.add_field(name='Query', value=f'```{query}```')
# 		embed.add_field(name='Result', value=f'```{res}```', inline=False)
#
# 		embed.set_author(name='Wolfram Alpha', icon_url='https://i.imgur.com/KFppH69.png')
# 		embed.set_footer(text='wolframalpha.com')
#
# 		if len(query) + len(res) > 1200:
# 			raise commands.CommandError('Wolfram response too long.')
#
# 		await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Wolfram(client))
