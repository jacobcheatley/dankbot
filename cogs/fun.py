import discord
from discord.ext import commands
import re
import random
from .rps import Gesture, gesture_map
from .utils import database
from threading import Lock

rps_description = 'ROCK: {}\nPAPER: {}\nSCISSORS: {}\nLIZARD: {}\nSPOCK: {}\n'.format(
    ', '.join(gesture_map[Gesture.rock]),
    ', '.join(gesture_map[Gesture.paper]),
    ', '.join(gesture_map[Gesture.scissors]),
    ', '.join(gesture_map[Gesture.lizard]),
    ', '.join(gesture_map[Gesture.spock])
)

default_total = {
    'win': 0,
    'loss': 0,
    'draw': 0
}

default_record = {
    'win': 0,
    'loss': 0,
    'draw': 0,
    'current_streak': 0,
    'win_streak': 0,
    'loss_streak': 0
}

locks = {}


class Fun:
    """Commands that serve no real purpose."""

    def __init__(self, bot):
        self.bot = bot
        self.rps_db = database.Database('rps.json')

    @commands.command()
    async def roll(self, dice: str):
        """Rolls dice in the format NdX+C."""
        dice_pattern = r'^(\d*)d(\d+)(?:(\+|-)(\d+))?'
        try:
            num_dice, size, sign, mod = re.findall(dice_pattern, dice)[0]
            dice_roll = sum((random.randint(1 if int(size) else 0, int(size)) for _ in range(int(num_dice or 1))))
            constant = eval('{}{}'.format(sign, mod)) if mod else 0
            await self.bot.say('Rolled a {}'.format(dice_roll + constant))
        except Exception as e:
            print(e)
            await self.bot.say('Invalid dice format (NdX+C)')

    @commands.command()
    async def flip(self):
        """Flips a coin."""
        await self.bot.say(random.choice(['Heads', 'Tails']))

    @commands.command(name='8ball', description='The Magic 8 Ball has the answers to all questions.')
    async def eightball(self, question: str = ''):
        """Shakes the Magic 8 Ball."""
        if question == '':
            await self.bot.say('Perhaps ask a question.')
        else:
            await self.bot.say(random.choice([
                'It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it',
                'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                'Reply hazy try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now',
                'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'My sources say no',
                'Outlook not so good', 'Very doubtful'
            ]))

    @commands.command(description='https://www.youtube.com/watch?v=wGlBwW7f5HA')
    async def lenny(self, number: int = None):
        """( ͡° ͜ʖ ͡°)"""
        lennies = ['( ͡° ͜ʖ ͡°)', '\\\\(ꗞ ͟ʖꗞ)/', '(ง⍤□⍤)ง', '[x╭╮x]', '(⚆ ͜ʖ⚆)', '\\\\( º  ͟ʖ º )/',
                   '(  つ ಠ ڡ ಠ C )', '( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)', '┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴', '( ͡°╭͜ʖ╮͡° )',
                   '[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]', '/╲/\\\\╭( ͡° ͡° ͜ʖ ͡° ͡°)╮/\\\\╱\\\\', '༼ つ  ͡° ͜ʖ ͡° ༽つ',
                   '( ͡ᵔ ͜ʖ ͡ᵔ )', '( ಠ ͜ʖರೃ)', '\\\\( ͠°ᗝ °)/', '( ͠°╭͜ʖ╮ °)', '\\\\( ͠° ͜ʖ °)/', '( ͡°ᴥ ͡°)',
                   '( ͡° ͟ʖ ͡°)', '乁(૦ઁ╭͜ʖ╮૦ઁ)ㄏ', '乁(๏‿‿๏)ㄏ', '(⌐■ ͜ʖ■)', '($ ͜ʖ$)', '\\\\(ಠ_ಠ)/']
        if number is None:
            await self.bot.say(random.choice(lennies))
        elif not (1 <= number <= len(lennies)):
            await self.bot.say('Number out of range (1 - {})'.format(len(lennies)))
        else:
            await self.bot.say(lennies[number - 1])

    @commands.group(pass_context=True, name='rps', aliases=['rpsls', '321', 'play'], description=rps_description,
                    invoke_without_command=True)
    async def rps(self, ctx: commands.Context, play: str):
        """Plays a game of rock-paper-scissors-lizard-Spock with DankBot."""
        player_gesture = None
        for gesture, symbols in gesture_map.items():
            if play.lower() in symbols:
                player_gesture = gesture
                break

        if player_gesture is None:
            await self.bot.say('Not a valid play. Try !help rps.')
            return

        player_id = ctx.message.author.id

        if player_id not in locks:
            locks[player_id] = Lock()

        dankbot_gesture = Gesture(random.randrange(1, 6))

        result = player_gesture.result_versus_bot(dankbot_gesture)
        await self.bot.say(result.message)

        draw = result.win is None
        win = result.win
        loss = not win and not draw

        with locks[player_id]:
            record = self.rps_db.get(player_id, default_record)
            updated_streak = 0
            if result.win:
                updated_streak = max(1, record['current_streak'] + 1)
            elif result.win is False:
                updated_streak = min(-1, record['current_streak'] - 1)
            await self.rps_db.put(player_id, {
                'win': record['win'] + 1 if win else record['win'],
                'loss': record['loss'] + 1 if loss else record['loss'],
                'draw': record['draw'] + 1 if draw else record['draw'],
                'current_streak': updated_streak,
                'win_streak': max(updated_streak, record['win_streak']),
                'loss_streak': max(-updated_streak, record['loss_streak'])
            })

    @rps.command(pass_context=True)
    async def record(self, ctx):
        """Gives your own personal record against DankBot."""
        record = self.rps_db.get(ctx.message.author.id, default_record)
        w = record['win']
        l = record['loss']
        streak = record['current_streak']
        lines = ['**Record for {}:**'.format(ctx.message.author.name),
                 '*Wins:* {}'.format(w),
                 '*Losses:* {}'.format(l),
                 '*W/L:* {:.2f}'.format(w / max(l, 1)),
                 '*Draws:* {}'.format(record['draw']),
                 '*Current Streak:* {}'.format(str(abs(streak)) + (' losses' if streak < 0 else ' wins')),
                 '*Longest Win Streak:* {}'.format(record['win_streak']),
                 '*Longest Loss Streak:* {}'.format(record['loss_streak'])]
        await self.bot.say('\n'.join(lines))

    @rps.command(pass_context=True)
    async def stats(self):
        """Gives stats about peoples battles against DankBot."""
        everything = self.rps_db.all().items()

        # TODO: Rework and simplify these submethods
        def wl(record: tuple):
            return record[1]['win'] / max(record[1]['loss'], 1)

        def basic_asc_sort(func):
            return sorted(everything, key=func, reverse=True)[:5]

        def asc_sort(key: str):
            return basic_asc_sort(lambda r: r[1][key])

        def find_by_id(id: str):
            return discord.utils.find(lambda m: m.id == id, self.bot.get_all_members())

        def reformat_record(record: tuple, key: str):
            return '{} ({})'.format(find_by_id(record[0]), record[1][key])

        def func_reformat_record(record: tuple, func):
            return '{} ({})'.format(find_by_id(record[0]), format(func(record), '.2f'))

        def reformat_all(records: [tuple], key: str, func=None):
            if func is None:
                return ', '.join(reformat_record(record, key) for record in records)
            else:
                return ', '.join(func_reformat_record(record, func) for record in records)

        def sum_key(key: str):
            return sum(record[1][key] for record in everything)

        lines = ['**Overall:**',
                 '*Wins:* {}'.format(sum_key('win')),
                 '*Losses:* {}'.format(sum_key('loss')),
                 '*Draws:* {}'.format(sum_key('draw')),
                 '**High Scores:**',
                 '*Most Wins:* {}'.format(reformat_all(asc_sort('win'), 'win')),
                 '*Most Losses:* {}'.format(reformat_all(asc_sort('loss'), 'loss')),
                 '*Most Draws:* {}'.format(reformat_all(asc_sort('draw'), 'draw')),
                 '*Best W/L:* {}'.format(reformat_all(basic_asc_sort(wl), '', func=wl)),
                 '*Best Win Streak:* {}'.format(reformat_all(asc_sort('win_streak'), 'win_streak')),
                 '*Worst Loss Streak:* {}'.format(reformat_all(asc_sort('loss_streak'), 'loss_streak'))]
        await self.bot.say('\n'.join(lines))


def setup(bot):
    bot.add_cog(Fun(bot))
