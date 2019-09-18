import discord, os
from discord.ext import commands

class Extensions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cogs.{extension}")
        print(f"Loaded cog {extension}")
        await ctx.send(f"Loaded extension {extension}")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        if extension == "extcommands":
            await ctx.send("You cant unload this!")
        self.bot.unload_extension(f"cogs.{extension}")
        print(f"Unloaded cog {extension}")
        await ctx.send(f"Unloaded extension {extension}")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        if extension == "all":
            print(f"reloading all Cogs")
            for filename in filter(lambda filename: filename.endswith(".py"), os.listdir("cogs")):
                cog_name = filename[:-3]
                self.bot.unload_extension(f"cogs.{cog_name}")
                self.bot.load_extension(f"cogs.{cog_name}")
            await ctx.send("Reloaded all extensions")
            return
        self.bot.unload_extension(f"cogs.{extension}")
        self.bot.load_extension(f"cogs.{extension}")
        print(f"Reloaded cog {extension}")
        await ctx.send(f"Reloaded extension {extension}")

def setup(bot):
    bot.add_cog(Extensions(bot))
