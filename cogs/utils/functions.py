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
