import discord
import re


class Replies:
    def __init__(self, bot):
        self.bot = bot
        self.r_regex = re.compile(r'(?:^|\s)/r/(\S+)')
        self.u_regex = re.compile(r'(?:^|\s)/u/(\S+)')

    async def on_message(self, message: discord.Message):
        if message.content.startswith(self.bot.command_prefix) or message.author.id == self.bot.user.id:
            return

        reply_lines = []

        r_matches = self.r_regex.findall(message.content)
        if r_matches:
            print(r_matches)
            subs = ['https://www.reddit.com/r/{}'.format(sub) for sub in r_matches]
            reply_lines.extend(subs)

        u_matches = self.u_regex.findall(message.content)
        if u_matches:
            print(u_matches)
            users = ['https://www.reddit.com/u/{}'.format(user) for user in u_matches]
            reply_lines.extend(users)

        if reply_lines:
            await self.bot.send_message(message.channel, '\n'.join(reply_lines))


def setup(bot):
    bot.add_cog(Replies(bot))
