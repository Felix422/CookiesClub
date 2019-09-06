import discord, logging, os, aiohttp
from discord.ext import commands
from config import BOT_TOKEN, COMMAND_PREFIX

logging.basicConfig(level=logging.ERROR)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
        command_prefix=COMMAND_PREFIX,
        case_insensitive=True
        )
        self.remove_command("help")

    async def on_connect(self):
        print("Connected to discord")

    async def on_ready(self):
        extensions = 0
        for filename in filter(lambda filename: filename.endswith(".py"), os.listdir("cogs")):
            cog_name = filename[:-3]
            extensions += 1
            self.load_extension(f"cogs.{cog_name}")
        print(f"Loaded {extensions} extensions")
        print("Initializing aiohttp")
        self.aiohttp = aiohttp.ClientSession(
            loop=self.loop,
            timeout=aiohttp.ClientTimeout(total=5)
        )
        print(f"Bot Logged in as {self.user.name} and ready for duty!")

Bot().run(BOT_TOKEN)
