from GameFrame import RoomObject, Globals


class Flag(RoomObject):
    def __init__(self, room, x, y, image_file_name):
        RoomObject.__init__(self, room, x, y)

        flag_image = self.load_image(image_file_name)
        self.set_image(flag_image, 32, 32)
