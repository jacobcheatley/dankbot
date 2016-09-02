import discord
from discord.ext import commands
from .utils import checks, config, functions


class Forwarding:
    """A class for forwarding information to the bot owner"""

    def __init__(self, bot):
        self.bot = bot
        self.owner = self.get_owner()
        self.last_sender = None

    def format_pm(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return '**I sent** \'{0.content}\'\nTo user **{0.channel.user}** @ {0.timestamp}.'.format(message)
        else:
            return '**I received** \'{0.content}\'\nFrom user **{0.channel.user}** @ {0.timestamp}.'.format(message)

    async def transfer_pm_info(self, message: discord.Message):
        await self.send_to_owner(self.format_pm(message))

    async def send_to_owner(self, content: str):
        if self.owner is None:
            self.owner = self.get_owner()

        await functions.send_long(self.bot, self.owner, content)

    def get_owner(self):
        return discord.utils.find(lambda m: m.id == config.owner_id, self.bot.get_all_members())

    @commands.group(hidden=True)
    @checks.is_owner()
    async def pm(self):
        """For personal message management"""
        pass

    @pm.command()
    async def review(self, user: discord.User, n: int=10):
        """Shows last n messages from a user to DankBot."""
        channel = discord.utils.find(lambda c: c.user == user, self.bot.private_channels)
        if channel is None:
            await self.bot.say('Can\'t find user messages.')
            return

        logs = []
        async for log in self.bot.logs_from(channel, n):
            logs.append(log)
        logs = reversed(logs)
        await self.bot.send_message(self.owner, '---START REVIEW---')
        await functions.send_long(self.bot, self.owner, '\n\n'.join(self.format_pm(log) for log in logs))
        await self.bot.send_message(self.owner, '---END REVIEW---')

    @pm.command(aliases=['s'])
    async def send(self, user: discord.User, *, content):
        """Sends a message to a user as DankBot."""
        await self.bot.send_message(user, content)

    @pm.command(aliases=['r'])
    async def reply(self, *, content):
        """Sends a reply back to the person who last sent a message."""
        if self.last_sender is None:
            await self.bot.say('No one to reply to to.')
            return
        await self.bot.send_message(self.last_sender, content)

    async def on_message(self, message: discord.Message):
        if not message.channel.is_private or message.channel.user.id == self.owner.id:
            return

        self.last_sender = message.author
        await self.transfer_pm_info(message)

    async def on_message_delete(self, message: discord.Message):
        content = '**Message in *{0.server.name}#{0.channel.name}* by *{0.author.name}* deleted:**\n' \
                  '\n' \
                  '\'{0.content}\'\n' \
                  '\n' \
                  '*Message time: {0.timestamp}*'.format(message)
        await self.send_to_owner(content)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return

        content = '**Message in *{0.server.name}#{0.channel.name}* by *{0.author.name}* edited:**\n' \
                  '\n' \
                  '*Previous:*\n' \
                  '\'{0.content}\'\n' \
                  '*New:*\n' \
                  '\'{1.content}\'\n' \
                  '\n' \
                  '*Message time: {0.timestamp}*'.format(before, after)
        await self.send_to_owner(content)


def setup(bot):
    bot.add_cog(Forwarding(bot))
