import discord.utils
from discord.ext import commands
from config import ALLOWED_CHANNELS

async def is_channel_allowed(ctx):
    return ctx.channel.name in ALLOWED_CHANNELS
