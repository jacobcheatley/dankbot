import discord
from discord.ext import commands
import time
from .utils import functions, database, checks
import datetime

fmt = '%Y-%m-%d %H:%M:%S'


class Info:
    """This category of things gives information, FYI."""

    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database('info.json')
        self.start_time = time.time()

    def member_info(self, member: discord.Member):
        member_id = member.id
        extra_info = self.db.get('extra_info', {})
        name = 'Not assigned.'
        desc = 'Not assigned.'
        if member_id in extra_info:
            name = extra_info[member_id]['name']
            desc = extra_info[member_id]['desc']
        return 'Info about {0.name} ({0.status}):\n' \
               '{0.avatar_url}\n' \
               'ID: {0.id}\n' \
               'Name: {1}\n' \
               'Description: {2}\n' \
               'Joined at: {0.joined_at}\n'.format(member, name, desc)

    @commands.command()
    async def whois(self, member: discord.Member):
        """Displays information about a mentioned user."""
        await self.bot.say(self.member_info(member))

    @commands.command(pass_context=True)
    async def whoami(self, ctx: commands.Context):
        """Displays information about yourself."""
        await self.bot.say(self.member_info(ctx.message.author))

    @commands.command()
    @checks.is_owner()
    async def describe(self, member: discord.Member, name: str, description: str):
        """Updates the name and description of a user."""
        extra_info = self.db.get('extra_info', {})
        extra_info[member.id] = {
            'name': name,
            'desc': description
        }
        await self.db.put('extra_info', extra_info)
        await self.bot.say('Updated member info.')

    @commands.command()
    async def uptime(self):
        """Displays bot uptime."""
        seconds = int(time.time() - self.start_time)
        await self.bot.say('Bot has been up for ' + functions.seconds_format(seconds) + '.')

    @commands.command(aliases=['add_event'])
    @checks.is_owner()
    async def event(self, name: str, *, content: str):
        """Adds an event to the summary info."""
        summaries = self.db.get('summaries', [])
        missed = self.db.get('missed', dict())

        summaries.append({
            'name': name,
            'content': content,
            'time': datetime.datetime.now().strftime(fmt)
        })
        await self.db.put('summaries', summaries)
        for k in missed:
            missed[k] += 1

        await self.bot.say('Added a new event to summaries: "{0}"'.format(name))

    @commands.command(aliases=['what_happened', '?'], pass_context=True)
    async def summary(self, ctx: commands.Context):
        """Gives a summary of the most recent few events you haven't caught up on."""

        missed = self.db.get('missed', dict())
        id = ctx.message.author.id
        events = 5
        if id in missed:
            events = min(5, missed[id])
        if events != 0:
            missed[id] = 0
            await self.db.put('missed', missed)

            summaries = self.db.get('summaries', [])
            current_time = datetime.datetime.now()
            stuff_to_say = '{0.mention}, since you last used summary:\n'.format(ctx.message.author)
            for summary in summaries[-events:]:
                time = datetime.datetime.strptime(summary['time'], fmt)
                time_delta = int((current_time - time).total_seconds())
                time_format = functions.seconds_format(time_delta)
                stuff_to_say += '{0} ago: **"{1}"** - *{2}*\n'.format(time_format, summary['name'], summary['content'])
            await self.bot.say(stuff_to_say)
        else:
            await self.bot.say('You are up to date.')


def setup(bot):
    bot.add_cog(Info(bot))
