from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 1
    FLAG = 3
    PREPARE = 4
    BAIT = 5
    JAIL = 6
    HOME = 7


class Red3(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.WAIT
        self.prev_x_enemy = 0

    def tick(self):
        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.FLAG:
            self.flag()
        elif self.curr_state == STATE.PREPARE:
            self.prepare()
        elif self.curr_state == STATE.BAIT:
            self.bait()
        elif self.curr_state == STATE.JAIL:
            self.jailedf()
        elif self.curr_state == STATE.HOME:
            self.gohome()
        else:
            self.curr_state = STATE.WAIT
    # 
    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        #Stay and or move close to the top border
        if self.x <= 644 or self.x >= 656:
            self.turn_towards(650, 600, Globals.FAST)
            self.drive_forward(Globals.FAST)
        # todo Check for enemies
        # if distance < 250 and bot.x > 650:
        #     self.curr_state = STATE.ATTACK
        # todo Wait for Bait
        
        else:
            self.curr_state = STATE.PREPARE
            # * self.curr_state = STATE.FLAG
    
    def prepare(self):
        Globals.red_bots[0].bot3ready = True
        if Globals.red_bots[0].bot4ready and Globals.red_bots[0].bot5ready:
            self.curr_state = STATE.BAIT

    def bait(self):
        bot, distance = self.closest_enemy_to_self(True)
        angle=abs(self.angleRelative(bot.x,bot.y))
        if self.x >= 1200 and self.y >= 650:
            self.curr_state = STATE.JAIL
        # ? move across border, evading enemies
        elif angle<60 and distance<200 and not self.has_flag:
            self.evadeBots()
        elif not self.has_flag:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            i = self.angleRelative(Globals.red_bots[0].x, Globals.red_bots[0].y)
            if i < 0 or i > 40:
                self.turn_towards(Globals.red_bots[0].x, Globals.red_bots[0].y, Globals.FAST)
            self.drive_forward(Globals.FAST)

    
    def jailedf(self):
        # todo - if jailbroken
        Globals.red_bots[0].bot3ready = False
        if not self.jailed:
            self.curr_state = STATE.HOME
    
    def gohome(self):
        # todo - move to upper position
        self.curr_state = STATE.WAIT
    
    
    """
    Helper Functions
    """
    # * Evade bots
    def evadeBots(self):
        closest_enemy, dist = self.closest_enemy_to_self(True)
        if self.angleRelative(closest_enemy.x,closest_enemy.y)<0:
            self.turn_right(Globals.MEDIUM)
        else:
            self.turn_left(Globals.MEDIUM)
        # Driving forward
        self.drive_forward(Globals.FAST)
        
    # * Get opposite direction from self, from winner 2020 code
    def oppositeDirection(self):
        closest_bot, dist = self.closest_enemy_to_self(True)
        pointX = self.x - closest_bot.x
        pointY = self.y - closest_bot.y
        return pointX,pointY
            
    def attack(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.turn_towards(bot.x, bot.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = STATE.WAIT

    def closest_enemy_to_flag(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.blue_flag.x, Globals.blue_flag.y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.blue_flag.x, Globals.blue_flag.y)
            
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance
    
    def closest_enemy_to_self(self, ignore):
        # todo - make more efficient
        closest_bot = Globals.blue_bots[0]
        closer_bot = Globals.red_bots[0] 
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         self.x, self.y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         self.x, self.y)
            for red_bot in Globals.red_bots:
                # * check enemy distance from self to bot from loop
                if curr_bot_dist < shortest_distance:
                    curr_teammate_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         self.x, self.y)
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
    def angleRelative(self,x,y):
        LEFT=False
        angle=self.NormalizedAngle(x,y)
        if self.angle-angle<0: LEFT=True
        diffangle=min(abs(self.angle-angle),360-abs(self.angle-angle))
        if LEFT: diffangle *= -1
        return diffangle

    def NormalizedAngle(self,x,y):
        angle = self.get_rotation_to_coordinate(x,y)
        if angle<0: angle+=360
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

