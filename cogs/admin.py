import discord
from discord.ext import commands
from .utils import checks, functions, database
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlparse


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database('admin.json')

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

    @commands.command()
    @checks.is_owner()
    async def ignore(self, *, member: discord.Member):
        """Globally ignores a member."""
        ignores = self.db.get('ignores', [])

        if member.id in ignores:
            await self.bot.say('That user is already ignored.')
            return

        ignores.append(member.id)
        await self.db.put('ignores', ignores)
        await self.bot.say('{0.name} has been ignored by DankBot.'.format(member))

    @commands.command()
    @checks.is_owner()
    async def unignore(self, *, member: discord.Member):
        """Unignores the member."""
        ignores = self.db.get('ignores', [])

        try:
            ignores.remove(member.id)
        except ValueError:
            pass
        else:
            await self.db.put('ignores', ignores)
            await self.bot.say('{0.name} has been unignored by DankBot.'.format(member))


def setup(bot):
    bot.add_cog(Admin(bot))
