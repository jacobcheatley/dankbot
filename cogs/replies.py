import discord
import re


class Replies:
    def __init__(self, bot):
        self.bot = bot
        self.r_regex = r'/r/([^\s/]+)'

    async def on_message(self, message: discord.Message):
        if message.content.startswith(self.bot.command_prefix) or message.author.id == self.bot.user.id:
            return
        r_matches = re.findall(self.r_regex, message.content)
        if r_matches:
            subs = ['https://www.reddit.com/r/{}'.format(sub) for sub in r_matches]
            await self.bot.send_message(message.channel, '\n'.join(subs))


def setup(bot):
    bot.add_cog(Replies(bot))
