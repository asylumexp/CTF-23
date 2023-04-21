from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    TIANSHUI = 0 # * Wait state
    HANDAN = 1 # * Strike state
    PINQLIANG = 2 # * Move to area state
    BAO = 3 # * Bait state
    BAIT_TRUE = 4 # * Prepare bait state
    EVADE = 5 # * Evade state
    JAIL = 6 # * Jail state

class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.TIANSHUI

    def tick(self):
        # * States
        if self.curr_state == STATE.PINQLIANG:
            self.PINQLIANG()
        elif self.curr_state == STATE.HANDAN:
            self.HANDAN()
        elif self.curr_state == STATE.TIANSHUI:
            self.TIANSHUI()
        elif self.curr_state == STATE.BAIT_TRUE:
            self.BAIT_TRUE()
        elif self.curr_state == STATE.BAO:
            self.BAO()
        elif self.curr_state == STATE.JAIL:
            self.JAIL()
        else:
            self.curr_state = STATE.TIANSHUI


    # * Moving to prepare area
    def PINQLIANG(self):
        # * Drive until in position in upper region
        if self.x <= 644 or self.x >= 656:
            self.turn_towards(650, 25, Globals.FAST)
            self.drive_forward(Globals.FAST)
        # * If that the area, start the bait prepare
        else:
            self.curr_state = STATE.BAIT_TRUE

    # * Attack State
    def HANDAN(self):
        # * Check for bot
        bot, distance = self.closest_enemy_to_bot()
        angle = self.angleRelative(bot.x,bot.y)
        self.turn_towards(bot.x, bot.y, Globals.SLOW)
        if distance<100 and angle<70:
                self.drive_forward(Globals.FAST)
        if distance>100:
            self.curr_state = STATE.TIANSHUI

    # * Waiting for other bait bots
    def BAIT_TRUE(self):
        Globals.red_bots[0].bot5ready = True
        if Globals.red_bots[0].bot3ready and Globals.red_bots[0].bot4ready:
            self.curr_state = STATE.BAO

    #  * Checking for enemies
    def TIANSHUI(self):
        bot, distance = self.closest_enemy_to_bot()
        if distance < 250:
            self.curr_state = STATE.HANDAN

        else:
            self.curr_state = STATE.PINQLIANG
            
    # * Bait state
    def BAO(self):
        bot, distance = self.closest_enemy_to_bot()
        distance = self.point_to_point_distance(self.x, self.y, bot.x, bot.y)
        angle=abs(self.angleRelative(bot.x,bot.y))
        if self.x >= 1200 and self.y >= 650:
            self.curr_state = STATE.JAIL
        elif angle<60 and distance<200 and not self.has_flag:
            self.evadeBots()
        elif not self.has_flag:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            i = self.angleRelative(Globals.red_bots[0].x, Globals.red_bots[0].y)
            if i < 0 or i > 50:
                self.turn_towards(Globals.red_bots[0].x, Globals.red_bots[0].y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            print("PASS, RED5 BAO()")


    # * Jail state
    def JAIL(self):
        Globals.red_bots[0].bot5ready = False
        if not self.jailed:
            self.curr_state = STATE.TIANSHUI

    # * Evade state
    def evadeBots(self):
        closest_enemy, null = self.closest_enemy_to_bot()
        if self.angleRelative(closest_enemy.x,closest_enemy.y)<0:
            self.turn_right(Globals.FAST)
        else:
            self.turn_left(Globals.FAST)

        # Driving forward
        self.drive_forward(Globals.FAST)
    
    # ** Helper Functions **
    
    # * get closest enemy to self
    def closest_enemy_to_bot(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.red_bots[4].x, Globals.red_bots[4].y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.red_bots[4].x, Globals.red_bots[4].y)
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance

    # * Get closest enemy to the flag
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
    
    # * Relative angle calculation
    def angleRelative(self,x,y):
        angle=self.NormalizedAngle(x,y)
        diffangle=min(abs(self.angle-angle),360-abs(self.angle-angle))
        return diffangle

    # * normalised angle calculation
    def NormalizedAngle(self,x,y):
        angle = self.get_rotation_to_coordinate(x,y)
        if angle<0: angle+=360
        return angle
