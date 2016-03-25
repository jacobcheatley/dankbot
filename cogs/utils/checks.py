import discord
from discord.ext import commands


def is_owner_check(message):
    return message.author.id == '132448107148476417'


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


def in_channel(*channels: str):
    return commands.check(lambda ctx: ctx.message.channel.name in channels)


def in_spam_channel():
    return in_channel('spam_allowed', 'spam')

# TODO: Config files
