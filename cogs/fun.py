import discord
from discord.ext import commands
import re
import random


class Fun:
    def __init__(self, bot):
        self.bot = bot

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
    async def eightball(self, question: str=''):
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
    async def lenny(self, number: int=None):
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


def setup(bot):
    bot.add_cog(Fun(bot))
