import discord, logging, os, aiohttp
from discord.ext import commands
from config import BOT_TOKEN, COMMAND_PREFIX

logging.basicConfig(level=logging.WARN)


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=COMMAND_PREFIX
        )

        self.remove_command("help")

    async def on_connect(self):
        print("Connected to discord")

    async def on_ready(self):

        for filename in filter(lambda filename: filename.endswith(".py"), os.listdir("cogs")):
            cog_name = filename[:-3]
            print(f"Loading {cog_name}")
            self.load_extension(f"cogs.{cog_name}")

        print("Initializing aiohttp")
        self.aiohttp = aiohttp.ClientSession(
            loop=self.loop,
            timeout=aiohttp.ClientTimeout(total=5)
        )

        await self.change_presence(status=discord.Status.online, activity=discord.Activity(name="all those bad suggestions", type=discord.ActivityType.watching))
        print("Changed presence")
        print(f"Bot Logged in as {self.user.name} and ready for duty!")

Bot().run(BOT_TOKEN)
