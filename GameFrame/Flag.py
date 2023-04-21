from GameFrame import RoomObject, Globals


class Flag(RoomObject):
    def __init__(self, room, x, y, image_file_name, flag_winner):
        RoomObject.__init__(self, room, x, y)
        self.flag_winner = flag_winner
        flag_image = self.load_image(image_file_name)
        self.set_image(flag_image, 32, 32)

    def step(self):
        if self.flag_winner == Globals.RED_FLAG_WINNER and self.x > Globals.SCREEN_WIDTH/2 or self.flag_winner == Globals.BLUE_FLAG_WINNER and self.x < Globals.SCREEN_WIDTH/2:
            Globals.winner = self.flag_winner
            self.room.running = False