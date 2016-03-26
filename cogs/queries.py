import discord
from discord.ext import commands
from .utils import checks, functions
import os
import wolframalpha

wolfram_client = wolframalpha.Client(os.environ['WOLFRAM_ID'])


class Queries:
    """Internet searching things!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.in_spam_channel()
    async def wolfram(self, ctx: commands.Context, *query: str):
        """Ask Wolfram Alpha something."""
        query_string = ' '.join(query)
        result = wolfram_client.query(query_string)
        pod_texts = []
        for pod in result.pods:
            pod_texts.append('**{0.title}**\n{0.img}'.format(pod))
        await functions.send_long(self.bot, ctx.message.channel, '\n'.join(pod_texts))

    # TODO: Add google, translate, define, meme, and so on


def setup(bot):
    bot.add_cog(Queries(bot))
