from GameFrame import Globals, Bot
import GameFrame.RedBot


class BlueBot(Bot):
    def __init__(self, room, x, y):
        Bot.__init__(self, room, x, y, Globals.BLUE_COLOUR, GameFrame.RedBot, BlueBot)
