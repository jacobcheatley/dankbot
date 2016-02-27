import discord
from discord.ext import commands
from .utils import database
import parsedatetime as pdt
import re
from pytz import timezone
import asyncio
from datetime import datetime


class Reminder:
    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database('reminders.json')
        self.cal = pdt.Calendar(constants=pdt.Constants(localeID='en_AU'))
        self.quote_regex = re.compile(r'"(.*)"')
        self.updater = bot.loop.create_task(self.update_reminders())

    @commands.command(pass_context=True, description='Use !remindme {time} "{message}". Your message must be quoted.')
    async def remindme(self, ctx):
        """Reminds you of something in a time."""
        try:
            m = self.quote_regex.search(ctx.message.content)
            time = ctx.message.content[10:m.start()]
            text = m.group()
            dt_obj, ret = self.cal.parseDT(time)
            reminders = self.db.get('reminders', [])
            reminders.append(
                {
                    'time': str(dt_obj),
                    'id': ctx.message.author.id,
                    'text': text
                }
            )
            await self.db.put('reminders', reminders)
            await self.bot.say('Reminding {} about {} - {}.'.format(ctx.message.author.mention, text, time))
        except:
            await self.bot.say('Invalid format. Use !remindme {time} "{message}". Try !remindme 1 minute "TOP KEK!"')

    async def update_reminders(self):
        try:
            while not self.bot.is_closed:
                current_time = datetime.now()
                reminders = self.db.get('reminders', [])
                to_remove = []
                for reminder in reminders:
                    t = datetime.strptime(reminder['time'], '%Y-%m-%d %I:%M:%S')
                    if t <= current_time:
                        to_remove.append(reminder)
                        await self.send_reminder(reminder)
                if to_remove:
                    for reminder in to_remove:
                        reminders.remove(reminder)
                    await self.db.put('reminders', reminders)
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            print('Error')
            pass

    async def send_reminder(self, reminder):
        member = discord.utils.find(lambda m: m.id == reminder['id'], self.bot.get_all_members())
        await self.bot.send_message(member, 'Reminding you about {}'.format(reminder['text']))


def setup(bot):
    bot.add_cog(Reminder(bot))
