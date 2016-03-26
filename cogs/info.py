import discord
from discord.ext import commands
import time


def member_info(member: discord.Member):
    return 'Info about {0.name} ({0.status}):\n' \
           '{0.avatar_url}\n' \
           'ID: {0.id}\n' \
           'Joined at: {0.joined_at}\n'.format(member)


class Info:
    """This category of things gives information, FYI."""

    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def whois(self, member: discord.Member):
        """Displays information about yourself."""
        await self.bot.say(member_info(member))

    @commands.command(pass_context=True)
    async def whoami(self, ctx: commands.Context):
        """Displays information about a mentioned user."""
        await self.bot.say(member_info(ctx.message.author))

    @commands.command()
    async def uptime(self):
        """Displays bot uptime."""
        seconds = int(time.time() - self.start_time)
        days = seconds // 86400
        seconds -= days * 86400
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds // 60
        seconds -= minutes * 60
        time_display = '{0}{1}{2}{3}'.format('' if days == 0 else str(days) + ' days, ',
                                             '' if hours == 0 else str(hours) + ' hours, ',
                                             '' if minutes == 0 else str(minutes) + ' minutes, ',
                                             str(seconds) + ' seconds.')
        await self.bot.say('Bot has been up for ' + time_display)


def setup(bot):
    bot.add_cog(Info(bot))
