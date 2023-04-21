from GameFrame import Flag, Globals


class BlueFlag(Flag):
    def __init__(self, room, x, y):
        Flag.__init__(self, room, x, y, 'flag_blue.png', Globals.BLUE_FLAG_WINNER)
        
        