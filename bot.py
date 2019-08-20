import discord, logging, os, aiohttp
from discord.ext import commands
from config import BOT_TOKEN, COMMAND_PREFIX

client = commands.Bot(command_prefix=COMMAND_PREFIX)
client.remove_command('help')
logging.basicConfig(level=logging.ERROR)


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=COMMAND_PREFIX
        )

        self.remove_command('help')

    async def on_ready(self):

        for filename in filter(lambda filename: filename.endswith('.py'), os.listdir('cogs')):
            cog_name = filename[:-3]
            print('Loading {}'.format(cog_name))
            self.load_extension('cogs.{}'.format(cog_name))

        print('Initializing aiohttp')
        self.aiohttp = aiohttp.ClientSession(
            loop=self.loop,
            timeout=aiohttp.ClientTimeout(total=5)
        )

        await self.change_presence(activity=discord.Activity(name="with the API", type=discord.ActivityType.playing))
        print(f"Bot Logged in as {self.user.name} and ready for duty!")

Bot().run(BOT_TOKEN)
