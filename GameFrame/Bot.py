from GameFrame import RoomObject
from GameFrame import Globals


class Bot(RoomObject):
    def __init__(self, room, x, y):
        RoomObject.__init__(self, room, x, y)
        self.starting_x = x
        self.starting_y = y
        self.has_flag = False
        self.jailed = False

    def step(self):
        if not self.jailed:
            self.frame()
            if self.x <= 0:
                self.blocked()
            elif self.x >= Globals.SCREEN_WIDTH - self.width:
                self.blocked()

            if self.y <= 0:
                self.blocked()
            elif self.y >= Globals.SCREEN_HEIGHT - self.height:
                self.blocked()

    def frame(self):
        pass

    def turn_left(self, speed=Globals.SLOW):
        if self.has_flag:
            self.rotate(40)
        elif speed == Globals.FAST:
            self.rotate(9)
        elif speed == Globals.MEDIUM:
            self.rotate(6)
        else:
            self.rotate(3)

    def turn_right(self, speed=Globals.SLOW):
        if self.has_flag:
            self.rotate(-40)
        elif speed == Globals.FAST:
            self.rotate(-9)
        elif speed == Globals.MEDIUM:
            self.rotate(-6)
        else:
            self.rotate(-3)

    def turn_towards(self, x, y, speed=Globals.SLOW):

        target_angle = int(self.get_rotation_to_coordinate(x, y))

        if target_angle < 0:
            target_angle = 360 + target_angle

        if self.curr_rotation <= 180:
            if self.curr_rotation + 2 < target_angle < self.curr_rotation + 180:
                self.turn_left(speed)
            else:
                self.turn_right(speed)
        else:
            if self.curr_rotation + 2 < target_angle < 360 or 0 <= target_angle < self.curr_rotation - 180:
                self.turn_left(speed)
            else:
                self.turn_right(speed)

    def drive_forward(self, speed=Globals.SLOW):
        if speed == Globals.FAST:
            self.move_in_direction(self.curr_rotation, Globals.FAST)
        elif speed == Globals.MEDIUM:
            self.move_in_direction(self.curr_rotation, Globals.MEDIUM)
        else:
            self.move_in_direction(self.curr_rotation, Globals.SLOW)

    def drive_backward(self):
        direction = self.curr_rotation - 180
        if direction < 0:
            direction = 360 + direction
        self.move_in_direction(direction, Globals.SLOW)
