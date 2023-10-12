from GameFrame import BlueBot, Globals
from enum import Enum

""" 
-3.2698548073713    SLOW = 2
-6.2698548073713    MEDIUM = 5
-9.54212546246344   FAST = 8
"""

class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    PREPARE = 4
    BAIT = 5
    JAIL = 6
    HOME = 7
    JAILBREAK = 8


class Blue3(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.curr_state = STATE.WAIT
        self.prev_x_enemy = 0
        try:
            self.set_image("Images/b3.png", 25, 25)
        except FileNotFoundError:
            print("hello this is me making a error checking for the set image we used images in our testing so we actually knew which bot was which if youre seeing this that means we again forgot to remove the set image for red3 which is awkward gotta say so bye have fun doing the competition.")


    def tick(self):
        if self.curr_state == STATE.WAIT:
            self.bait_bot_prepare(self, 650, 600, STATE.PREPARE)
        elif self.curr_state == STATE.ATTACK:
            self.general_bot_attack(self, STATE.WAIT)
        elif self.curr_state == STATE.PREPARE:
            self.bait_bot_wait(self, STATE.BAIT)
        elif self.curr_state == STATE.BAIT:
            self.bait_bot_bait(self, STATE.JAIL)
        elif self.curr_state == STATE.JAIL:
            self.general_bot_jailed(self, STATE.HOME)
        elif self.curr_state == STATE.HOME:
            self.general_bot_return(self, STATE.WAIT)
        elif self.curr_state == STATE.JAILBREAK:
            self.jailbreak(self, STATE.JAILBREAK)
        else:
            self.curr_state = STATE.WAIT
    
    @staticmethod
    def bait_bot_prepare(self: BlueBot, bait_position_x: int, bait_position_y: int, wait_state: STATE):
        """Prepare State for the Bait bots
        
        This state moves the bot to the bait position and will in the future attack others

        Args:
            bait_position_x (int): x pos for bait position.
            bait_position_y (int): y pos for bait position.
            wait_state (STATE): state for waiting until all bots are ready.
        """
        
        bot, distance = Globals.blue_bots[2].closest_enemy_to_flag()
        # Stay and or move close to the top border
        if self.x <= bait_position_x - 6 or self.x >= bait_position_x + 6:
            self.turn_towards(bait_position_x, bait_position_y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        # todo Check for enemies
        # if distance < 250 and bot.x > 650:
        #     self.curr_state = STATE.ATTACK
        # todo Wait for Bait
        else:
            self.curr_state = wait_state
            # * self.curr_state = STATE.FLAG

    @staticmethod
    def return_home(self: BlueBot, STATE):
        # if self.x <= self.psuedoflagx-40 or self.x >= self.psuedoflagx-50:
        # self.turn_towards(self.psuedoflagx-40, Globals.blue_flag.y, Globals.FAST)
        # self.drive_forward(Globals.FAST)
        if (self.point_to_point_distance(self.x, self.y, self.psuedoflagx, Globals.red_flag.y) > 40):
            # i = self.angleRelative(self.psuedoflagx, Globals.blue_flag.y)
            # if i < 0 or i > 40:
            self.turn_towards(self.psuedoflagx, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = STATE.WAIT

    @staticmethod
    def bait_bot_wait(self: BlueBot, bait_state: STATE):
        """Bait Bot Waiting State
        
        This is the state where the bots wait in until they are ready to go attack.

        Args:
            self (RedBot): the bot that is calling this.
            bait_state (STATE): the state for attacking.
        """
        if self == Globals.blue_bots[2]:
             Globals.blue_bots[0].bot3ready = True
        elif self == Globals.blue_bots[3]:
            Globals.blue_bots[0].bot4ready = True
        elif self == Globals.blue_bots[4]:
            Globals.blue_bots[0].bot5ready = True

        if Globals.blue_bots[0].bot3ready and Globals.blue_bots[0].bot4ready and Globals.blue_bots[0].bot5ready:
            self.curr_state = bait_state

    @staticmethod
    def wait(self: BlueBot, return_state: STATE):
        bot, distance = self.closest_enemy_to_self(True)
        if distance < 200:
            self.curr_state = STATE.ATTACK
        else:
            bot_jailed = False
            for team_bot in Globals.red_bots:
                if team_bot.jailed:
                    bot_jailed = True
                    break
            if bot_jailed:
                self.curr_state = STATE.JAILBREAK

    @staticmethod
    def bait_bot_bait(self: BlueBot, jail_state):
        """Bait Bot Bait State

        Args:
            self (RedBot): the bot that is calling the function.
            jail_state (_type_): the state to change to once jailed.
        """
        bot, distance = Globals.blue_bots[2].closest_enemy_to_self(self, True)
        angle = abs(Globals.blue_bots[2].angleRelative(self, bot.x, bot.y))
        if self.x >= 1100 and self.y >= 600:
            self.curr_state = jail_state
        # ? move across border, evading enemies
        elif angle < 60 and distance < 200 and not self.has_flag:
            Globals.blue_bots[2].evadeBots(self)
        elif not self.has_flag:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            i = Globals.blue_bots[2].angleRelative(self, Globals.blue_bots[0].x, Globals.blue_bots[0].y)
            if i < 0 or i > 45:
                self.turn_towards(Globals.blue_bots[0].x, Globals.blue_bots[0].y, Globals.SLOW)
            self.drive_forward(Globals.FAST)

    @staticmethod
    def general_bot_jailed(self: BlueBot, return_state: STATE):
        """Jailed State 

        Args:
            self (RedBot): the bot calling the function
            return_state (STATE): state to change to once out of jail.
        """
        # todo - if jailbroken
        
        if self == Globals.blue_bots[2]:
             Globals.blue_bots[0].bot3ready = False
        elif self == Globals.blue_bots[3]:
            Globals.blue_bots[0].bot4ready = False
        elif self == Globals.blue_bots[4]:
            Globals.blue_bots[0].bot5ready = False
        if not self.jailed:
            self.curr_state = STATE.HOME
    
    @staticmethod
    def general_bot_return(self: BlueBot, next_state):
        """Jailed State 

        Args:
            self (RedBot): the bot calling the function
            next_state (STATE): state to change to immediately.
        """
        # todo - move to upper position
        self.curr_state = next_state


    @staticmethod
    def general_bot_attack(self: BlueBot, return_state: STATE):
        """General Attack State 

        Args:
            self (RedBot): the bot calling the function
            next_state (STATE): state to change to immediately.
        """
        # * Check for bot
        bot, distance = Globals.blue_bots[2].closest_enemy_to_self(self, False)
        angle = Globals.blue_bots[2].angleRelative(self, bot.x, bot.y)
        self.turn_towards(bot.x, bot.y, Globals.SLOW)
        self.drive_forward(Globals.FAST)


    """
    Helper Functions
    """

        
    def closest_enemy_to_flag(self: BlueBot):
        closest_bot = Globals.red_bots[0]
        shortest_distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, Globals.red_flag.x, Globals.red_flag.y
        )
        for curr_bot in Globals.red_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, Globals.red_flag.x, Globals.red_flag.y
            )

            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance
        
    # * Evade bots\
    @staticmethod
    def evadeBots(self: BlueBot):
        closest_bot, dist = Globals.blue_bots[2].closest_enemy_to_self(self, True)
        pointX = self.x - closest_bot.x
        pointY = self.y - closest_bot.y
        if Globals.blue_bots[2].angleRelative(self, closest_bot.x, closest_bot.y) < 0:
            self.turn_towards(pointX, pointY)
        elif Globals.blue_bots[2].angleRelative(self, closest_bot.x, closest_bot.y) < 100:
            self.turn_left(Globals.MEDIUM)
        else:
            self.turn_right(Globals.MEDIUM)
        self.drive_forward(Globals.FAST)

    @staticmethod
    def closest_enemy_to_self(self: BlueBot, ignore):
       # todo - make more efficient
        closest_bot = Globals.red_bots[0]
        closer_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y, self.x, self.y)
        for curr_bot in Globals.red_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y, self.x, self.y)
            for blue_bot in Globals.blue_bots:
                # * check enemy distance from self to bot from loop
                if curr_bot_dist < shortest_distance:
                    curr_teammate_dist = self.point_to_point_distance(
                        curr_bot.x, curr_bot.y, self.x, self.y
                    )
                    # * check if teammate is closer
                    if curr_teammate_dist < curr_bot_dist and not ignore:
                        shortest_distance = curr_bot_dist
                        closest_bot = curr_bot
                    elif ignore:
                        shortest_distance = curr_bot_dist
                        closest_bot = curr_bot

        return closest_bot, shortest_distance

    def flag(self):
        if self.has_flag:
            self.turn_towards(400, self.y)
            self.drive_forward(Globals.FAST)
        elif self.rect.right >= Globals.SCREEN_WIDTH / 2:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
    
    @staticmethod
    def angleRelative(self: BlueBot, x, y):
        LEFT = False
        angle = Globals.blue_bots[2].NormalizedAngle(self, x, y)
        if self.angle - angle < 0:
            LEFT = True
        diffangle = min(abs(self.angle - angle), 360 - abs(self.angle - angle))
        if LEFT:
            diffangle *= -1
        return diffangle

    @staticmethod
    def NormalizedAngle(self: BlueBot, x, y):
        angle = self.get_rotation_to_coordinate(x, y)
        if angle < 0:
            angle += 360
        return angle
    
    @staticmethod
    def jailbreak(self: BlueBot, return_state: STATE):
        bot_jailed = False
        for team_bot in Globals.blue_bots:
            if team_bot.jailed:
                bot_jailed = True
                break
        if not bot_jailed:
            self.curr_state = return_state
        else:
            angle = self.angleRelative(75, 100)
            self.turn_towards(75, 100, Globals.FAST)
            if angle < 120:
                self.drive_forward(Globals.FAST)
