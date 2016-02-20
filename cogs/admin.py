import discord
from discord.ext import commands
from .utils import checks, functions
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlparse


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def paste(self, ctx: commands.Context, url: str):
        """Pastes a pastebin URL."""
        url = urlparse(url)
        new_url = ''.join(['http://' if url.scheme == '' else url.scheme + '://',
                           url.netloc,
                           '/raw' if not url.path.startswith('/raw') else '',
                           url.path])
        try:
            with urlopen(new_url) as response:
                html = response.read()
                await functions.send_long(self.bot, ctx.message.channel, html.decode('utf-8'))
        except urllib.request.URLError:
            pass

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def clear(self, ctx: commands.Context, n: int=10):
        """Clears the bot's messages."""
        deleted = 0
        async for message in self.bot.logs_from(ctx.message.channel):
            if message.author.id == self.bot.user.id:
                deleted += 1
                await self.bot.delete_message(message)
            if deleted == n:
                return

    @commands.command(pass_context=True, name='eval')
    @checks.is_owner()
    async def eval_command(self, ctx: commands.Context):
        """Evaluates a Python 3.5.1 expression."""
        str_to_eval = ctx.message.content[ctx.message.content.find(' '):]
        try:
            await self.bot.say(eval(str_to_eval))
        except Exception as e:
            await self.bot.whisper(e)


def setup(bot):
    bot.add_cog(Admin(bot))
