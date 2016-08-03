import discord
from discord.ext import commands
from .utils import config
import pytz


class Quotes:
    def __init__(self, bot):
        self.bot = bot
        self.quotes_channel = self.get_channel()

    def get_channel(self):
        return discord.utils.find(lambda c: c.id == config.quotes_channel_id, self.bot.get_all_channels())

    async def do_quote(self, ctx: commands.Context, message_id: int, target_channel: discord.Channel):
        message = await self.bot.get_message(ctx.message.channel, str(message_id))

        if message is None:
            await self.bot.say('Can\'t find message.')
            return

        content = '"{}" by {} in <#{}> @ {}'.format(message.content, message.author.name, message.channel.id,
                                                    self.nz_time_format(message.timestamp))
        await self.bot.send_message(target_channel, content)

    @commands.group(pass_context=True, invoke_without_command=True)
    async def quote(self, ctx: commands.Context, message_id: int):
        """Quotes a message by ID.
        To get the ID, click on the cog on the message and copy ID (enable Developer Mode).
        """

        await self.do_quote(ctx, message_id, ctx.message.channel)

    @quote.command(pass_context=True)
    async def archive(self, ctx: commands.Context, message_id: int):
        """Quotes a message and sticks it in #quotes as well."""

        await self.do_quote(ctx, message_id, self.quotes_channel)

    async def on_ready(self):
        self.quotes_channel = self.get_channel()

    @staticmethod
    def nz_time_format(utc_dt):
        local_tz = pytz.timezone('Pacific/Auckland')
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt).strftime('%H:%M:%S %d/%m')


def setup(bot):
    bot.add_cog(Quotes(bot))
