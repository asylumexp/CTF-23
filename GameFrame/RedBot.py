from GameFrame import Globals, Bot
import GameFrame.BlueBot


class RedBot(Bot):
    def __init__(self, room, x, y):
        Bot.__init__(self, room, x, y, Globals.RED_COLOUR, GameFrame.BlueBot, RedBot)
