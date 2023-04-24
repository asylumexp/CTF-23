from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    PREPARE = 4
    BAIT = 5
    JAIL = 6
    HOME = 7


class Red3(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.WAIT
        self.prev_x_enemy = 0
        self.set_image("Images/r3.png", 25, 25)

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
        else:
            self.curr_state = STATE.WAIT
    
    @staticmethod
    def bait_bot_prepare(self: RedBot, bait_position_x: int, bait_position_y: int, wait_state: STATE):
        """Prepare State for the Bait bots
        
        This state moves the bot to the bait position and will in the future attack others

        Args:
            bait_position_x (int): x pos for bait position.
            bait_position_y (int): y pos for bait position.
            wait_state (STATE): state for waiting until all bots are ready.
        """
        
        bot, distance = Globals.red_bots[2].closest_enemy_to_flag()
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
    def bait_bot_wait(self: RedBot, bait_state: STATE):
        """Bait Bot Waiting State
        
        This is the state where the bots wait in until they are ready to go attack.

        Args:
            self (RedBot): the bot that is calling this.
            bait_state (STATE): the state for attacking.
        """
        if self == Globals.red_bots[2]:
             Globals.red_bots[0].bot3ready = True
        elif self == Globals.red_bots[3]:
            Globals.red_bots[0].bot4ready = True
        elif self == Globals.red_bots[4]:
            Globals.red_bots[0].bot5ready = True

        if Globals.red_bots[0].bot3ready and Globals.red_bots[0].bot4ready and Globals.red_bots[0].bot5ready:
            self.curr_state = bait_state
    
    @staticmethod
    def bait_bot_bait(self: RedBot, jail_state):
        """Bait Bot Bait State

        Args:
            self (RedBot): the bot that is calling the function.
            jail_state (_type_): the state to change to once jailed.
        """
        bot, distance = Globals.red_bots[2].closest_enemy_to_self(True)
        angle = abs(Globals.red_bots[2].angleRelative(bot.x, bot.y))
        if self.x >= 1100 and self.y >= 600:
            self.curr_state = jail_state
        # ? move across border, evading enemies
        elif angle < 60 and distance < 200 and not self.has_flag:
            Globals.red_bots[2].evadeBots()
        elif not self.has_flag:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            i = Globals.red_bots[2].angleRelative(Globals.red_bots[0].x, Globals.red_bots[0].y)
            if i < 0 or i > 40:
                self.turn_towards(Globals.red_bots[0].x, Globals.red_bots[0].y, Globals.FAST)
            self.drive_forward(Globals.FAST)

    @staticmethod
    def general_bot_jailed(self: RedBot, return_state: STATE):
        """Jailed State 

        Args:
            self (RedBot): the bot calling the function
            return_state (STATE): state to change to once out of jail.
        """
        # todo - if jailbroken
        
        if self == Globals.red_bots[2]:
             Globals.red_bots[0].bot3ready = False
        elif self == Globals.red_bots[3]:
            Globals.red_bots[0].bot4ready = False
        elif self == Globals.red_bots[4]:
            Globals.red_bots[0].bot5ready = False

        if not self.jailed:
            self.curr_state = STATE.HOME
    
    @staticmethod
    def general_bot_return(self: RedBot, next_state):
        """Jailed State 

        Args:
            self (RedBot): the bot calling the function
            next_state (STATE): state to change to immediately.
        """
        # todo - move to upper position
        self.curr_state = STATE.WAIT

    @staticmethod
    def general_bot_attack(self: RedBot, return_state: STATE, dist = 250):
        """General Attack State 

        Args:
            self (RedBot): the bot calling the function
            next_state (STATE): state to change to immediately.
            dist (int, default: 250): maximum distance to target them
        """
        bot, distance = Globals.red_bots[2].closest_enemy_to_flag()
        if distance < dist:
            self.turn_towards(bot.x, bot.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = return_state

    """
    Helper Functions
    """

    # * Evade bots
    def evadeBots(self):
        closest_enemy, dist = Globals.red_bots[2].closest_enemy_to_self(True)
        if self.angleRelative(closest_enemy.x, closest_enemy.y) < 0:
            self.turn_right(Globals.MEDIUM)
        else:
            self.turn_left(Globals.MEDIUM)
        # Driving forward
        self.drive_forward(Globals.FAST)

    # * Get opposite direction from self, from winner 2020 code
    def oppositeDirection(self):
        closest_bot, dist = Globals.red_bots[2].closest_enemy_to_self(True)
        pointX = self.x - closest_bot.x
        pointY = self.y - closest_bot.y
        return pointX, pointY

    def closest_enemy_to_flag(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, Globals.blue_flag.x, Globals.blue_flag.y
        )
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, Globals.blue_flag.x, Globals.blue_flag.y
            )

            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance

    def closest_enemy_to_self(self, ignore):
        # todo - make more efficient
        closest_bot = Globals.blue_bots[0]
        closer_bot = Globals.red_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y, self.x, self.y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y, self.x, self.y)
            for red_bot in Globals.red_bots:
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
            self.turn_towards(Globals.SCREEN_WIDTH, self.y)
            self.drive_forward(Globals.FAST)
        elif self.rect.right >= Globals.SCREEN_WIDTH / 2:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)

    def angleRelative(self, x, y):
        LEFT = False
        angle = self.NormalizedAngle(x, y)
        if self.angle - angle < 0:
            LEFT = True
        diffangle = min(abs(self.angle - angle), 360 - abs(self.angle - angle))
        if LEFT:
            diffangle *= -1
        return diffangle

    def NormalizedAngle(self, x, y):
        angle = self.get_rotation_to_coordinate(x, y)
        if angle < 0:
            angle += 360
        return angle


# from ast import Global
# from GameFrame import RedBot, Globals
# import random
# from enum import Enum
# class STATE(Enum):
#     WAIT = 1
#     ATTACK = 2
#     JAIL_BREAK = 3

# class Red3(RedBot):
#     def __init__(self, room, x, y):
#         RedBot.__init__(self, room, x, y)
#         self.initial_wait = random.randint(30, 90)
#         self.wait_count = 0
#         self.curr_state = STATE.WAIT
#         self.set_image("Images/master.png", 25, 25)

#     def tick(self):
#         self.turn_towards(0, Globals.SCREEN_HEIGHT/2, 30)
#         self.drive_forward(Globals.FAST)
#     #     if self.curr_state == STATE.WAIT:
#     #         self.wait()
#     #     elif self.curr_state == STATE.ATTACK:
#     #         self.attack()
#     #     elif self.curr_state == STATE.JAIL_BREAK:
#     #         self.jailbreak()
#     #     else:
#     #         self.curr_state = STATE.WAIT

#     # def wait(self):
#     #     bot, distance = self.closest_enemy_to_flag()
#     #     if distance < 250:
#     #         self.curr_state = STATE.ATTACK
#     #     else:
#     #         bot_jailed = False
#     #         for team_bot in Globals.blue_bots:
#     #             if team_bot.jailed:
#     #                 bot_jailed = True
#     #                 break
#     #         if bot_jailed:
#     #             self.curr_state = STATE.JAIL_BREAK

#     # def attack(self):
#     #     bot, distance = self.closest_enemy_to_flag()
#     #     if distance < 250:
#     #         self.turn_towards(bot.x, bot.y, Globals.FAST)
#     #         self.drive_forward(Globals.FAST)
#     #     else:
#     #         self.curr_state = STATE.WAIT

#     # def jailbreak(self):
#     #     bot_jailed = False
#     #     for team_bot in Globals.red_bots:
#     #         if team_bot.jailed:
#     #             bot_jailed = True
#     #             break
#     #     if not bot_jailed:
#     #         self.curr_state = STATE.WAIT
#     #     else:
#     #         self.turn_towards(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT, Globals.FAST)
#     #         self.drive_forward(Globals.FAST)

#     # def closest_enemy_to_flag(self):
#     #     closest_bot = Globals.red_bots[0]
#     #     shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
#     #                                                      Globals.red_flag.x, Globals.red_flag.y)
#     #     for curr_bot in Globals.red_bots:
#     #         curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
#     #                                                      Globals.red_flag.x, Globals.red_flag.y)
#     #         if curr_bot_dist < shortest_distance:
#     #             shortest_distance = curr_bot_dist
#     #             closest_bot = curr_bot

#     #     return closest_bot, shortest_distance
