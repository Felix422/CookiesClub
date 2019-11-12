from discord.utils import get

async def is_channel_allowed(ctx):
    channel_allowed = ctx.channel.id in ctx.bot.allowed_channels
    user_allowed = ctx.author.guild_permissions.manage_guild
    return channel_allowed or user_allowed
