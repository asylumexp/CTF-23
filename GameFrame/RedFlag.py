from GameFrame import Flag, Globals


class RedFlag(Flag):
    def __init__(self, room, x, y):
        Flag.__init__(self, room, x, y, 'flag_red.png', Globals.RED_FLAG_WINNER)
        