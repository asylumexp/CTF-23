from GameFrame import RoomObject, Globals


class RedFlag(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        red_flag_image = self.load_image('flag_red.png')
        self.set_image(red_flag_image, 32, 32)

    def step(self):
        if self.x > Globals.SCREEN_WIDTH/2:
            Globals.winner = 'Red'
            self.room.running = False
