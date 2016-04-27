from discord.ext import commands
import os
from cogs.utils import checks

bot = commands.Bot(command_prefix='!', description='This bot is Dank.')

initial_extensions = [
    'cogs.admin',
    'cogs.conversation',
    'cogs.fun',
    'cogs.info',
    'cogs.replies',
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


@bot.command(hidden=True)
@checks.is_owner()
async def load(*, module: str):
    """Loads a module by name."""
    module = module.strip()
    try:
        bot.load_extension(module)
    except Exception as e:
        await bot.say('{}: {}'.format(type(e).__name__, e))
    else:
        await bot.say('\U0001f44c')


@bot.command(hidden=True)
@checks.is_owner()
async def unload(*, module : str):
    """Unloads a module."""
    module = module.strip()
    try:
        bot.unload_extension(module)
    except Exception as e:
        await bot.say('{}: {}'.format(type(e).__name__, e))
    else:
        await bot.say('\U0001f44c')


if __name__ == '__main__':
    bot.run(os.environ['DISCORD_TOKEN'])
