import discord
from discord.ext import commands

class Main(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Staff')
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cogs.{extension}")
        print(f"Loaded cog {extension}")
        await ctx.send(f"Loaded extension {extension}")

    @load.error
    async def load_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.ExtensionAlreadyLoaded):
            await ctx.send("Extension already loaded")
            return
        elif isinstance(error, discord.ext.commands.errors.ExtensionNotFound):
            await ctx.send("Extension not found")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You dont have permission for this")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)

    @commands.command()
    @commands.has_role('Staff')
    async def unload(self, ctx, extension):
        if extension == "main":
            await ctx.send("You cant unload main!")
        self.bot.unload_extension(f"cogs.{extension}")
        print(f"Unloaded cog {extension}")
        await ctx.send(f"Unloaded extension {extension}")

    @unload.error
    async def unload_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.ExtensionNotFound):
            await ctx.send("Extension not found")
            return
        elif isinstance(error, discord.ext.commands.errors.ExtensionNotLoaded):
            await ctx.send("Extension not loaded")
        elif isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You dont have permission for this")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)

    @commands.command()
    @commands.has_role('Staff')
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f"cogs.{extension}")
        self.bot.load_extension(f"cogs.{extension}")
        print(f"Reloaded cog {extension}")
        await ctx.send(f"Reloaded extension {extension}")

    @reload.error
    async def reload_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.ExtensionNotFound):
            await ctx.send("Extension not found")
            return
        elif isinstance(error, discord.ext.commands.errors.ExtensionNotLoaded):
            await ctx.send("Extension not loaded")
            return
        elif isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You dont have permission for this")
            return
        else:
            await ctx.send("Something broke, contact Felix422")
            print(error)

def setup(bot):
    bot.add_cog(Main(bot))
