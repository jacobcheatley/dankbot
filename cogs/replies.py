import discord
import re


class Replies:
    def __init__(self, bot):
        self.bot = bot
        self.r_regex = r'/r/([^\s/]+)'
        self.u_regex = r'/u/([^\s/]+)'

    async def on_message(self, message: discord.Message):
        if message.content.startswith(self.bot.command_prefix) or message.author.id == self.bot.user.id:
            return

        reply_lines = []

        r_matches = re.findall(self.r_regex, message.content)
        if r_matches:
            subs = ['https://www.reddit.com/r/{}'.format(sub) for sub in r_matches]
            reply_lines.extend(subs)

        u_matches = re.findall(self.u_regex, message.content)
        if r_matches:
            users = ['https://www.reddit.com/u/{}'.format(user) for user in u_matches]
            reply_lines.extend(users)

        if reply_lines:
            await self.bot.send_message(message.channel, '\n'.join(reply_lines))


def setup(bot):
    bot.add_cog(Replies(bot))
