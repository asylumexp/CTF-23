from GameFrame import Bot, Globals, RedFlag
import GameFrame.BlueBot


class RedBot(Bot):
    def __init__(self, room, x, y):
        Bot.__init__(self, room, x, y)
        red_bot_image = self.load_image('bot_red.png')
        self.set_image(red_bot_image, 25, 25)

        self.rotate(90)

        self.register_collision_object('Blue1')
        self.register_collision_object('Blue2')
        self.register_collision_object('Blue3')
        self.register_collision_object('Blue4')
        self.register_collision_object('Blue5')
        self.register_collision_object('RedFlag')
        self.register_collision_object('Red1')
        self.register_collision_object('Red2')
        self.register_collision_object('Red3')
        self.register_collision_object('Red4')
        self.register_collision_object('Red5')

    def frame(self):
        if self.has_flag:
            if self.x < Globals.SCREEN_WIDTH / 2 + Globals.SCREEN_WIDTH / 4:
                Globals.red_flag.x = self.x - Globals.red_flag.rect.width - 2
                Globals.red_flag.y = self.y

                if Globals.red_flag.x <= 0:
                    Globals.red_flag.x = 0

                if Globals.red_flag.y <= 0:
                    Globals.red_flag.y = 0
                elif self.y + Globals.red_flag.rect.height >= Globals.SCREEN_HEIGHT:
                    Globals.red_flag.y = Globals.SCREEN_HEIGHT - Globals.red_flag.rect.height
            else:
                self.has_flag = False

        if self.x < Globals.SCREEN_WIDTH / 2:
            Globals.red_enemy_side_time += 1
            distance = self.point_to_point_distance(self.x, self.y, Globals.red_flag.x, Globals.red_flag.y)
            if self.has_flag:
                Globals.red_enemy_side_time += 50
            elif distance < 50:
                Globals.red_enemy_side_time += 30
            elif distance < 150:
                Globals.red_enemy_side_time += 20
            elif distance < 250:
                Globals.red_enemy_side_time += 10

        try:
            self.tick()
        except Exception:
            print("Red Exception occurred\n")

    def tick(self):
        pass

    def handle_collision(self, other):
        if isinstance(other, RedFlag):
            self.has_flag = True
            for bot in Globals.red_bots:
                if bot.has_flag and bot is not self:
                    self.has_flag = False
                    break
        elif isinstance(other, GameFrame.BlueBot):
            if self.x < Globals.SCREEN_WIDTH / 2 and not other.jailed:
                self.has_flag = False
                self.curr_rotation = 0
                self.rotate(90)
                self.x = Globals.SCREEN_WIDTH - 36
                self.y = Globals.SCREEN_HEIGHT - 40
                self.jailed = True
        elif isinstance(other, RedBot):
            if not other.jailed:
                self.jailed = False
