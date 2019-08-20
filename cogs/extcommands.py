import discord
from discord.ext import commands

class Main(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        print(f"Loaded cog {extension}")
        await ctx.send(f"Loaded extension {extension}")

    @commands.command()
    async def unload(self, ctx, extension):
        if extension == "main":
            await ctx.send("You cant unload main!")
        self.client.unload_extension(f"cogs.{extension}")
        print(f"Unloaded cog {extension}")
        await ctx.send(f"Unloaded extension {extension}")

    @commands.command()
    async def reload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        self.client.load_extension(f"cogs.{extension}")
        print(f"Reloaded cog {extension}")
        await ctx.send(f"Reloaded extension {extension}")

    @load.error
    async def load_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.ExtensionAlreadyLoaded):
            await ctx.send("Extension already loaded")
            return
        elif isinstance(error, discord.ext.commands.errors.ExtensionNotFound):
            await ctx.send("Extension not found")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)

    @unload.error
    async def unload_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.ExtensionNotFound):
            await ctx.send("Extension not found")
            return
        elif isinstance(error, discord.ext.commands.errors.ExtensionNotLoaded):
            await ctx.send("Extension not loaded")
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)

    @reload.error
    async def reload_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.ExtensionNotFound):
            await ctx.send("Extension not found")
            return
        elif isinstance(error, discord.ext.commands.errors.ExtensionNotLoaded):
            await ctx.send("Extension not loaded")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)

def setup(client):
    client.add_cog(Main(client))
