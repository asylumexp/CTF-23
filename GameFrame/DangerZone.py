from GameFrame import RoomObject


class DangerZone(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)

        self.set_image(self.load_image("danger_circle.png"), 150, 150)

