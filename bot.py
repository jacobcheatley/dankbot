from discord.ext import commands
import os
from cogs.utils import checks

bot = commands.Bot(command_prefix='!', description='This bot is Dank.')

initial_extensions = [
    'cogs.admin',
    'cogs.conversation',
    'cogs.fun',
    'cogs.info',
    # 'cogs.reminder',
    'cogs.tags',
    'cogs.queries'
]


@bot.event
async def on_ready():
    print('Logged in as {}.'.format(bot.user.name))

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))


@bot.event
async def on_message(message):
    admin = bot.get_cog('Admin')

    if admin is not None and not checks.is_owner_check(message):
        if message.author.id in admin.db.get('ignores', []):
            return

    await bot.process_commands(message)


if __name__ == '__main__':
    bot.run(os.environ['DISCORD_BOT_USER'], os.environ['DISCORD_BOT_PASS'])
