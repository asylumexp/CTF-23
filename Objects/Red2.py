from GameFrame import RedBot, Globals
import random


class Red2(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(30, 90)
        self.wait_count = 0

    def tick(self):
        if self.wait_count < self.initial_wait:
            self.wait_count += 1
        else:
            if self.has_flag:
                self.turn_towards(Globals.SCREEN_WIDTH, self.y)
                self.drive_forward(Globals.FAST)
            elif self.rect.right >= Globals.SCREEN_WIDTH / 2:
                self.turn_towards(self.starting_x - 400, self.starting_y, Globals.FAST)
                self.drive_forward(Globals.FAST)
            else:
                self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
                self.drive_forward(Globals.FAST)
