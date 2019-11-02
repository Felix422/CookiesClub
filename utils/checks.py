import discord.utils
from discord.ext import commands

async def is_channel_allowed(ctx):
    channel_allowed = ctx.channel.id in ctx.bot.allowed_channels
    user_allowed = get(ctx.guild.roles, name="Staff") in ctx.author.roles
    return channel_allowed or user_allowed
