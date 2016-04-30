import discord
from discord.ext import commands
from .utils import database
from random import choice

tfh_triggers = ['we need to build a wall',
                '10 feet higher',
                'make mexico pay for it',
                'ten feet higher',
                '10ft higher',
                'ten ft higher'
                ]
tfh_fmt = '**{}**\n**THE WALL JUST GOT TEN FEET HIGHER!**\nTotal Height: {}ft'
tfh_messages = [
    'JET FUEL CAN\'T MELT STEEL DREAMS',
    'My God it\'s full of ~~stars~~ real American pride',
    'Finally, a wall not made in China!',
    'Trump would be proud',
    'Sticks and stones may break my bones, but Trump will still build his wall.',
    'The thought of building Trump\'s wall fills you with DETERMINATION.',
    'Will this be the weapon to surpass Mexigear?',
    'What the fuck did you just say about me you little cuck?',
    'The Mexicans won\'t be able to nimbly navigate around this one.',
    'https://www.youtube.com/watch?v=G1ms-Oog4rs&feature=youtu.be',
    'The Height/Energy ratio is too low. WE NEED HIGHER ENERGY!',
    'Wall for President 2016',
    'With a small loan of a million dollars...',
    'Your *WALL* is evolving!',
    'In this world, it\'s TRUMP or be STUMPED!',
    'Nimble Navigation - No time for relaxation',
    'Silly Bernie, bricks are for walls!',
    'You can\'t Bern down this wall!',
    'He said higher, get building',
    'Good Fences Make Good Neighbors, Good Walls Make America Great Again',
    'The wall just doesn\'t stop, does it?',
    'Just another brick in the wall.',
    'Don\'t we have the BEST bots?!',
    'Taller than Kasich\'s pancake stack! With a drizzle of maple syrup, the wall has grown an extra 10 feet!',
    'With a small loan of a million bricks...',
    'Get building!',
    'https://i.sli.mg/OTpiJE.jpg',
    'Don\'t talk to me or my wall ever again',
    'Trumpity Trump Trump Trump',
    'Trump Wall: Building dreams and making memes since 2016',
    'We\'re going to have a big beautiful door in the middle!',
    'Another one, another one... And another one',
    'http://i.imgur.com/VkOqpZ8.png',
    'Our bricks will blot out the sun',
    'Taller than Bernie\'s cuckshed!',
    'Donald Trump: Adds +10 to WALL HEIGHT',
    'Build, dammit!',
    'Help! I\'ve fallen and I just got stumped by Trump.',
    'https://www.youtube.com/watch?v=qlIGom24qqc'
]


class Trump:
    """You can't stump the Trump."""

    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database('trump.json')

    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return

        if any((trigger in message.content.lower() for trigger in tfh_triggers)):
            wall_height = self.db.get('wall_height', 20) + 10
            await self.bot.send_message(message.channel, tfh_fmt.format(choice(tfh_messages), wall_height))
            await self.db.put('wall_height', wall_height)
        pass


def setup(bot):
    bot.add_cog(Trump(bot))
