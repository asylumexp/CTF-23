from GameFrame import Globals, RoomObject
import GameFrame.Flag
import traceback


class Bot(RoomObject):
    def __init__(self, room, x, y, bot_colour, other_team_bot, my_team_bot):
        RoomObject.__init__(self, room, x, y)
        self.starting_x = x
        self.starting_y = y
        self.has_flag = False
        self.jailed = False
        self.depth = 500

        self.OTHER_TEAM_BOT_OBJECT = other_team_bot
        self.MY_TEAM_BOT_OBJECT = my_team_bot

        # Create instance variables and function references dependent on Red or Blue
        if bot_colour == Globals.BLUE_COLOUR:
            self.FLAG_TO_STEAL_WINNER = Globals.BLUE_FLAG_WINNER
            self.START_DIRECTION = -90
            self.MY_TEAM_BOTS = Globals.blue_bots
            self.JAIL_POSITION = (Globals.GAME_AREA_WIDTH_MIN + 25, Globals.GAME_AREA_HEIGHT_MIN + 25)
            self.IMAGE = "bot_blue.png"
            self.FLAG_NAME = "BlueFlag"
            self.COLOUR_STRING = "Blue"
            self.COLOUR = Globals.BLUE_COLOUR
            self.on_enemy_side = self.on_enemy_side_blue
            self.set_flag_position = self.set_flag_position_blue
            self.get_flag = self.get_flag_blue
            self.set_local_flag_height = self.set_local_flag_height_blue
            self.add_points_close_to_flag = self.add_points_close_to_flag_blue
            self.distance_to_flag = self.distance_to_flag_blue
        else:
            self.FLAG_TO_STEAL_WINNER = Globals.RED_FLAG_WINNER
            self.START_DIRECTION = 90
            self.MY_TEAM_BOTS = Globals.red_bots
            self.JAIL_POSITION = (Globals.GAME_AREA_WIDTH_MAX - 25, Globals.GAME_AREA_HEIGHT_MAX - 25)
            self.IMAGE = "bot_red.png"
            self.FLAG_NAME = "RedFlag"
            self.COLOUR_STRING = "Red"
            self.COLOUR = Globals.RED_COLOUR
            self.on_enemy_side = self.on_enemy_side_red
            self.set_flag_position = self.set_flag_position_red
            self.get_flag = self.get_flag_red
            self.set_local_flag_height = self.set_local_flag_height_red
            self.add_points_close_to_flag = self.add_points_close_to_flag_red
            self.distance_to_flag = self.distance_to_flag_red

        bot_image = self.load_image(self.IMAGE)
        self.set_image(bot_image, 25, 25)

        self.rotate(self.START_DIRECTION)
        self.FLAG_HEIGHT = 0

        self.register_collision_object("Red1")
        self.register_collision_object("Red2")
        self.register_collision_object("Red3")
        self.register_collision_object("Red4")
        self.register_collision_object("Red5")
        self.register_collision_object("Blue1")
        self.register_collision_object("Blue2")
        self.register_collision_object("Blue3")
        self.register_collision_object("Blue4")
        self.register_collision_object("Blue5")
        self.register_collision_object(self.FLAG_NAME)

    def step(self):
        if not self.jailed:
            self.frame()
            if self.x <= Globals.GAME_AREA_WIDTH_MIN:
                self.blocked()
            elif self.x >= Globals.GAME_AREA_WIDTH_MAX - self.width:
                self.blocked()

            if self.y <= Globals.GAME_AREA_HEIGHT_MIN:
                self.blocked()
            elif self.y >= Globals.GAME_AREA_HEIGHT_MAX - self.height:
                self.blocked()

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

    def frame(self):
        if self.has_flag:
            if self.FLAG_HEIGHT == 0:
                self.set_local_flag_height()
            if self.on_enemy_side(Globals.SCREEN_WIDTH / 4):
                # keep the flag behind self
                flag_buffer = self.get_flag().rect.width + 2
                flag_x = self.x + flag_buffer if self.COLOUR == Globals.BLUE_COLOUR else self.x - flag_buffer
                flag_y = self.y

                # keep the flag in bounds x
                if flag_x >= Globals.GAME_AREA_WIDTH_MAX - 34:
                    flag_x = Globals.GAME_AREA_WIDTH_MAX - 34
                if flag_x <= Globals.GAME_AREA_WIDTH_MIN:
                    flag_x = Globals.GAME_AREA_WIDTH_MIN

                # keep the flag in bounds y
                if flag_y <= Globals.GAME_AREA_HEIGHT_MIN:
                    flag_y = Globals.GAME_AREA_HEIGHT_MIN + 2
                elif self.y + self.FLAG_HEIGHT >= Globals.GAME_AREA_HEIGHT_MAX:
                    flag_y = Globals.GAME_AREA_HEIGHT_MAX - self.FLAG_HEIGHT

                self.set_flag_position(flag_x, flag_y)
            else:
                self.has_flag = False

        if self.on_enemy_side():
            add_points = 1
            distance = self.distance_to_flag()
            if self.has_flag:
                add_points += 50
            elif distance < 50:
                add_points += 30
            elif distance < 150:
                add_points += 20
            elif distance < 250:
                add_points += 10

            self.add_points_close_to_flag(add_points)

        # Run the specific bot logic
        try:
            self.tick()
        except Exception:
            print(traceback.format_exc())

    def tick(self):
        pass

    def handle_collision(self, other):
        # Grab the victory flag if my teammate does not have it
        if isinstance(other, GameFrame.Flag) and other.flag_winner == self.FLAG_TO_STEAL_WINNER:
            self.has_flag = True
            for bot in self.MY_TEAM_BOTS:
                if bot.has_flag and bot is not self:
                    self.has_flag = False
                    break
        # Send me to jail on contact with enemy on their side
        elif isinstance(other, self.OTHER_TEAM_BOT_OBJECT):
            if self.on_enemy_side() and not other.jailed:
                self.has_flag = False
                self.curr_rotation = 0
                self.rotate(self.START_DIRECTION)
                self.x, self.y = self.JAIL_POSITION
                self.jailed = True
        # Get let out of jail by teammates
        elif isinstance(other, self.MY_TEAM_BOT_OBJECT):
            if not other.jailed:
                self.jailed = False

    def on_enemy_side_blue(self, additional_buffer=0):
        return self.rect.right > Globals.SCREEN_WIDTH / 2 - additional_buffer

    def on_enemy_side_red(self, additional_buffer=0):
        return self.x < Globals.SCREEN_WIDTH / 2 + additional_buffer

    # Helper method to set the global flag x and y depending on what colour the bot is
    @staticmethod
    def set_flag_position_blue(x, y):
        Globals.blue_flag.x = x
        Globals.blue_flag.y = y

    @staticmethod
    def set_flag_position_red(x, y):
        Globals.red_flag.x = x
        Globals.red_flag.y = y

    # Helper method to get the global flag x and y depending on what colour the bot is
    @staticmethod
    def get_flag_blue():
        return Globals.blue_flag

    @staticmethod
    def get_flag_red():
        return Globals.red_flag

    # Helper set the flag height
    def set_local_flag_height_blue(self):
        self.FLAG_HEIGHT = Globals.blue_flag.rect.height

    def set_local_flag_height_red(self):
        self.FLAG_HEIGHT = Globals.red_flag.rect.height

    # Helper method to add to the global scores of each team
    @staticmethod
    def add_points_close_to_flag_blue(points):
        Globals.blue_enemy_side_time += points

    @staticmethod
    def add_points_close_to_flag_red(points):
        Globals.red_enemy_side_time += points

    def distance_to_flag_blue(self):
        return self.point_to_point_distance(
            self.x,
            self.y,
            Globals.blue_flag.x,
            Globals.blue_flag.y
        )

    def distance_to_flag_red(self):
        return self.point_to_point_distance(
            self.x,
            self.y,
            Globals.red_flag.x,
            Globals.red_flag.y
        )
