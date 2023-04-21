from GameFrame import Bot, Globals, Flag

class GenericBot(Bot):
    def __init__(self, room, x, y):
        Bot.__init__(self, room, x, y)

        bot_image = self.load_image(self.IMAGE)
        self.set_image(bot_image, 25, 25)

        self.rotate(self.START_DIRECTION)
        self.FLAG_HEIGHT = 0

        self.register_collision_object('Red1')
        self.register_collision_object('Red2')
        self.register_collision_object('Red3')
        self.register_collision_object('Red4')
        self.register_collision_object('Red5')
        self.register_collision_object('Blue1')
        self.register_collision_object('Blue2')
        self.register_collision_object('Blue3')
        self.register_collision_object('Blue4')
        self.register_collision_object('Blue5')
        self.register_collision_object(self.FLAG_NAME)

    def frame(self):
        if self.has_flag:
            if self.FLAG_HEIGHT == 0:
                self.set_local_flag_height()    
            if self.on_enemy_side(Globals.SCREEN_WIDTH / 4):
                #keep the flag behind self
                flag_buffer = (self.get_flag().rect.width + 2)
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
            distance = self.point_to_point_distance(self.x, self.y, self.get_flag().x, self.get_flag().y)
            if self.has_flag:
                add_points += 50
            elif distance < 50:
                add_points += 30
            elif distance < 150:
                add_points += 20
            elif distance < 250:
                add_points+= 10
            
            self.add_points_close_to_flag(add_points)

        #Run the specific bot logic
        #todo could add in some custom exception handling for students
        try:
            self.tick()
        except Exception:
            print(self.COLOUR_STRING + " Exception occurred\n")

    def tick(self):
        pass

    def handle_collision(self, other):
        #Grab the victory flag if my teammate does nto have it
        if isinstance(other, Flag) and other.flag_winner == self.FLAG_TO_STEAL_WINNER:
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

    def on_enemy_side(self, additional_buffer = 0):
        if self.COLOUR == Globals.BLUE_COLOUR:
            return self.rect.right > Globals.SCREEN_WIDTH / 2 - additional_buffer
        elif self.COLOUR == Globals.RED_COLOUR:
            return self.x < Globals.SCREEN_WIDTH / 2 + additional_buffer