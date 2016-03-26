import discord
from discord.ext import commands


def segment_length(text):
    if len(text) < 2000:
        return len(text)

    for sep in '\n".':
        pos = text.rfind(sep, 0, 1999)
        if pos != -1:
            return pos
    return 2000


async def send_long(bot: commands.Bot, channel: discord.Channel, content: str):
    text_blocks = content.split('```')
    in_code_block = True if content.startswith('```') else False
    for text_part in text_blocks:
        while text_part:
            length = segment_length(text_part)
            await bot.send_message(channel, '{0}{1}{0}'.format('```' if in_code_block else '', text_part[:length]))
            text_part = text_part[length:]
        in_code_block = not in_code_block


def seconds_format(seconds: int):
    weeks, seconds = divmod(seconds, 604800)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    w_str = '' if weeks == 0 else str(weeks) + ' week{}, '.format('' if weeks == 1 else 's')
    d_str = '' if days == 0 else str(days) + ' day{}, '.format('' if days == 1 else 's')
    h_str = '' if hours == 0 else str(hours) + ' hour{}, '.format('' if hours == 1 else 's')
    m_str = '' if minutes == 0 else str(minutes) + ' minute{}, '.format('' if minutes == 1 else 's')
    s_str = str(seconds) + ' second{}'.format('' if seconds == 1 else 's')
    return '{0}{1}{2}{3}{4}'.format(w_str, d_str, h_str, m_str, s_str)
