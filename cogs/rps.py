from enum import Enum


class RPSResult:
    def __init__(self, win=None, message=''):
        self.win = win
        self.message = message


class Gesture(Enum):
    rock = 1
    paper = 2
    scissors = 3
    lizard = 4
    spock = 5

    def __str__(self):
        return gesture_map[self][0]

    def result_versus_bot(self, bot):
        if self is bot:
            return RPSResult(win=None, message='{} vs {} is a draw.'.format(str(self), str(bot)))

        if bot in gesture_winning[self]:
            return RPSResult(win=True, message='Your {0} {1} Dankbot\'s {2}. You win!'.format(
                str(self), gesture_winning[self][bot], str(bot)
            ))
        else:
            return RPSResult(win=False, message='Dankbot\'s {0} {1} your {2}. You lose!'.format(
                str(bot), gesture_winning[bot][self], str(self)
            ))


# Probably hard to see in most editors.
gesture_map = {
    Gesture.rock: ['💎', '✊', '👊', '👍', 'rock'],
    Gesture.paper: ['📃', '📄', '✋', '📜', '📖', 'paper'],
    Gesture.scissors: ['✂', '✌', 'scissors'],
    Gesture.lizard: ['🐉', '🐲', '🐍', 'lizard'],
    Gesture.spock: ['🖖', 'spock']
}

gesture_winning = {
    Gesture.rock: {Gesture.lizard: 'crushes', Gesture.scissors: 'smashes'},
    Gesture.paper: {Gesture.rock: 'covers', Gesture.spock: 'disproves'},
    Gesture.scissors: {Gesture.paper: 'cuts', Gesture.lizard: 'decapitates'},
    Gesture.lizard: {Gesture.paper: 'eats', Gesture.spock: 'poisons'},
    Gesture.spock: {Gesture.rock: 'vaporises', Gesture.scissors: 'smashes'}
}