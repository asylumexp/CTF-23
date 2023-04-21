from GameFrame import BlueBot, Globals
from enum import Enum


class STATE(Enum):
    TIANSHUI = 0 # * Wait state
    HANDAN = 1 # * Strike state
    PINQLIANG = 2 # * Move to area state
    BAO = 3 # * Bait state
    BAIT_TRUE = 4 # * Prepare bait state
    EVADE = 5 # * Evade state
    JAIL = 6 # * Jail state

class Blue3(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.curr_state = STATE.TIANSHUI

    def tick(self):
        #print(self.curr_state, self.x, self.y)
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
        bot, dista = self.closest_enemy_to_flag()
        if dista < 250:
            self.curr_state = STATE.HANDAN
        elif self.x <= 594 or self.x >= 606:
            self.turn_towards(600, 100, Globals.FAST)
            self.drive_forward(Globals.FAST)
        # * If that the area, start the bait prepare
        else:
            self.curr_state = STATE.BAIT_TRUE

    # * Attack State
    def HANDAN(self):
        bot, dista = self.closest_enemy_to_flag()
        # todo - attack bots
        if dista <= 200 and bot.x < 650:
            if dista < 200 and dista > 100:
                i = self.angleRelative(bot.x + 30, bot.y)
                #print(i)
                if i < 0 or i > 40:
                    self.turn_towards(bot.x + 30, bot.y, Globals.FAST)
                else:
                    self.drive_forward(Globals.FAST)
            elif dista < 100:
                self.turn_towards(bot.x + 30, bot.y, Globals.FAST)
                self.drive_forward(Globals.FAST)
        elif dista > 300:
            self.curr_state = STATE.TIANSHUI

    # * Waiting for other bait bots
    def BAIT_TRUE(self):
        bot, dista = self.closest_enemy_to_flag()
        self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
        Globals.blue_bots[0].bot3ready = True
        if Globals.blue_bots[0].bot4ready and Globals.blue_bots[0].bot5ready:
            self.curr_state = STATE.BAO

    #  * Checking for enemies
    def TIANSHUI(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.curr_state = STATE.HANDAN
        else:
            self.curr_state = STATE.PINQLIANG
            
    # * Bait state
    def BAO(self):
        bot, distance = self.closest_enemy_to_bot()
        distance = self.point_to_point_distance(self.x, self.y, bot.x, bot.y)
        angle=abs(self.angleRelative(bot.x,bot.y))
        if self.x <= 50 and self.y < 100:
            self.JAIL()
        elif angle<90 and distance<100 and not self.has_flag:
            self.evadeBots()
        elif not self.has_flag:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            i = self.angleRelative(Globals.blue_bots[0].x, Globals.blue_bots[0].y)
            if i < 0 or i > 40:
                self.turn_towards(Globals.blue_bots[0].x, Globals.blue_bots[0].y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            print("PASS, RED5 BAO()")


    # * Jail state
    def JAIL(self):
        self.curr_state == STATE.JAIL
        Globals.red_bots[0].bot3ready = False
        if not self.jailed:
            self.curr_state = STATE.TIANSHUI

    # * Evade state
    def evadeBots(self):
        closest_enemy, null = self.closest_enemy_to_bot()
        if self.angleRelative(closest_enemy.x,closest_enemy.y)>0:
            self.turn_right(Globals.FAST)
        else:
            self.turn_left(Globals.FAST)
        # Driving forward
        self.drive_forward(Globals.FAST)
    
    # ** Helper Functions **
    
    # * get closest enemy to self
    def closest_enemy_to_bot(self):
        closest_bot = Globals.red_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.blue_bots[4].x, Globals.blue_bots[4].y)
        for curr_bot in Globals.red_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.blue_bots[4].x, Globals.blue_bots[4].y)
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance

    # * Get closest enemy to the flag
    def closest_enemy_to_flag(self):
        closest_bot = Globals.red_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.red_flag.x, Globals.red_flag.y)
        for curr_bot in Globals.red_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.red_flag.x, Globals.red_flag.y)
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
