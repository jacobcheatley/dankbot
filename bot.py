from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!', description='This bot is Dank.')

initial_extensions = [
    'cogs.admin',
    'cogs.conversation',
    'cogs.fun',
    'cogs.info',
    'cogs.reminder',
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


if __name__ == '__main__':
    bot.run(os.environ['DISCORD_BOT_USER'], os.environ['DISCORD_BOT_PASS'])
