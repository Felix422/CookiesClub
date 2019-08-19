import discord, logging, os, aiohttp
from discord.ext import commands
from config import BOT_TOKEN,COMMAND_PREFIX

client = commands.Bot(command_prefix=COMMAND_PREFIX)
client.remove_command('help')
logging.basicConfig(level=logging.ERROR)

class Bot(commands.Bot):

    def __init__(self, client):
        self.client = client

    @client.event
    async def on_ready(self):
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(name="with the API", type=discord.ActivityType.playing))
        print(f"Bot Logged in as {client.user.name} and ready for duty!")
        self.aiohttp = aiohttp.ClientSession(
				timeout=aiohttp.ClientTimeout(total=5)
			)

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

client.run(BOT_TOKEN)
