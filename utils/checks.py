import discord.utils
from discord.ext import commands
from config import ALLOWED_CHANNELS

async def is_channel_allowed(ctx):
    channel_allowed = ctx.channel.name in ALLOWED_CHANNELS
    user_allowed = discord.utils.get(ctx.guild.roles, name="Staff") in ctx.author.roles
    return channel_allowed or user_allowed
