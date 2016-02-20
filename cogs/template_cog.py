import discord
from discord.ext import commands


class Conversation:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(Conversation(bot))
