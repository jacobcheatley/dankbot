import discord
from discord.ext import commands
from .utils import checks
from .lib import chatterbotapi as cb
import time

factory = cb.ChatterBotFactory()


class ConversationInfo:
    def __init__(self, session, channel):
        self.session = session
        self.channel = channel
        self.last_message_time = time.time()


class Conversation:
    """Because sometimes DankBot gets lonely."""

    def __init__(self, bot):
        self.bot = bot
        self.conversations = {}

    @commands.command(pass_context=True, name='talk')
    async def start_convo(self, ctx: commands.Context):
        """Starts talking with DankBot."""
        if ctx.message.author.id in self.conversations:
            return
        await self.bot.say('Starting a conversation with {}.'.format(ctx.message.author.mention))
        chatter_bot = factory.create(cb.ChatterBotType.CLEVERBOT)
        session = chatter_bot.create_session()
        self.conversations[ctx.message.author.id] = ConversationInfo(session, ctx.message.channel)

    @commands.command(pass_context=True, name='shutup')
    async def end_convo(self, ctx: commands.Context):
        """Tells DankBot to shut up and stop talking."""
        if ctx.message.author.id not in self.conversations:
            return
        await self.bot.say('Ending a conversation with {}'.format(ctx.message.author.mention))
        self.conversations.pop(ctx.message.author.id)

    @commands.command(name='stopall')
    @checks.is_owner()
    async def stop_all(self):
        """Brutally cuts out DankBot's voice box."""
        await self.bot.say('Ending all conversations.')
        self.conversations.clear()

    async def on_message(self, message: discord.Message):
        if message.content.startswith(self.bot.command_prefix):
            return
        author_id = message.author.id
        if author_id in self.conversations and self.conversations[author_id].channel == message.channel:
            convo = self.conversations[author_id]
            if convo.last_message_time + 120 < time.time():
                self.conversations.pop(author_id)
            else:
                convo.last_message_time = time.time()
                await self.bot.send_message(message.channel, convo.session.think(message.content))


def setup(bot):
    bot.add_cog(Conversation(bot))
