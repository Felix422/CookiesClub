import discord, logging, os, aiohttp, asyncpg
from discord.ext import commands
from config import BOT_TOKEN, COMMAND_PREFIX, DB_BIND

logging.basicConfig(level=logging.ERROR)

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
        command_prefix=COMMAND_PREFIX,
        case_insensitive=True,
        help_command=None
        )

    async def on_connect(self):
        print("Connected to discord")

    async def on_ready(self):
        extensions = 0
        for filename in filter(lambda filename: filename.endswith(".py"), os.listdir("cogs")):
            cog_name = filename[:-3]
            extensions += 1
            self.load_extension(f"cogs.{cog_name}")
        print(f"Loaded {extensions} extensions")
        print("Initializing AIOHTTP client session")
        self.aiohttp = aiohttp.ClientSession(
            loop=self.loop,
            timeout=aiohttp.ClientTimeout(total=5)
        )
        print("Connecting to Database")
        self.db = await asyncpg.create_pool(DB_BIND)

        print(f"Bot Logged in as {self.user.name} and ready for duty!")

Bot().run(BOT_TOKEN)
