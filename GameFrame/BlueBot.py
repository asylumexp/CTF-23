from GameFrame import Bot, Globals, BlueFlag
import GameFrame.RedBot


class BlueBot(Bot):
    def __init__(self, room, x, y):
        Bot.__init__(self, room, x, y)
        blue_bot_image = self.load_image('bot_blue.png')
        self.set_image(blue_bot_image, 25, 25)

        self.rotate(-90)

        self.register_collision_object('Red1')
        self.register_collision_object('Red2')
        self.register_collision_object('Red3')
        self.register_collision_object('Red4')
        self.register_collision_object('Red5')
        self.register_collision_object('BlueFlag')
        self.register_collision_object('Blue1')
        self.register_collision_object('Blue2')
        self.register_collision_object('Blue3')
        self.register_collision_object('Blue4')
        self.register_collision_object('Blue5')

    def frame(self):
        if self.has_flag:
            if self.x > Globals.SCREEN_WIDTH/2 - Globals.SCREEN_WIDTH / 4:
                Globals.blue_flag.x = self.x + self.rect.width + 2
                Globals.blue_flag.y = self.y

                if Globals.blue_flag.x >= Globals.SCREEN_WIDTH - 34:
                    Globals.blue_flag.x = Globals.SCREEN_WIDTH - 34

                if Globals.blue_flag.y <= 0:
                    Globals.blue_flag.y = 2
                elif self.y + Globals.blue_flag.rect.height >= Globals.SCREEN_HEIGHT:
                    Globals.blue_flag.y = Globals.SCREEN_HEIGHT - Globals.blue_flag.rect.height
            else:
                self.has_flag = False

        if self.x > Globals.SCREEN_WIDTH / 2:
            Globals.blue_enemy_side_time += 1
            distance = self.point_to_point_distance(self.x, self.y, Globals.blue_flag.x, Globals.blue_flag.y)
            if self.has_flag:
                Globals.blue_enemy_side_time += 50
            elif distance < 50:
                Globals.blue_enemy_side_time += 30
            elif distance < 150:
                Globals.blue_enemy_side_time += 20
            elif distance < 250:
                Globals.blue_enemy_side_time += 10


        try:
            self.tick()
        except Exception:
            print("Blue Exception occurred\n")

    def tick(self):
        pass

    def handle_collision(self, other):
        if isinstance(other, BlueFlag):
            self.has_flag = True
            for bot in Globals.blue_bots:
                if bot.has_flag and bot is not self:
                    self.has_flag = False
                    break
        elif isinstance(other, GameFrame.RedBot):
            if self.rect.right > Globals.SCREEN_WIDTH / 2 and not other.jailed:
                self.has_flag = False
                self.curr_rotation = 0
                self.rotate(-90)
                self.x = 20
                self.y = 20
                self.jailed = True
        elif isinstance(other, BlueBot):
            if not other.jailed:
                self.jailed = False
