from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    PREPARE = 3
    BAIT = 4
    JAIL = 5
    HOME = 6


class Red4(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.WAIT

    def tick(self):
        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
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

    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        # todo Check for enemies
        if distance < 250:
           self.attack()
        # * Stay and or move close to the top border
        if self.x <= 644 or self.x >= 656:
            self.turn_towards(650, 250, Globals.FAST)
            self.drive_forward(Globals.FAST)
        # * Wait for Bait
        else:
            self.curr_state = STATE.PREPARE
    
    def prepare(self):
        bot, distance = self.closest_enemy_to_flag()
        # todo Check for enemies
        Globals.red_bots[0].bot4ready = True
        if distance < 250:
           self.curr_state = STATE.ATTACK
        elif Globals.red_bots[0].bot3ready and Globals.red_bots[0].bot5ready:
            self.curr_state = STATE.BAIT

    def bait(self):
        bot, distance = self.closest_enemy_to_self(True)
        angle=abs(self.angleRelative(bot.x,bot.y))
        if self.x >= 1200 and self.y >= 650:
            self.curr_state = STATE.JAIL
        # ? move across border, evading enemies
        elif (angle<90 and distance<250) and not self.has_flag and self.point_to_point_distance(self.x,self.y,Globals.red_flag.x,Globals.red_flag.y)>150:
            self.evadeBots()
        elif not self.has_flag:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            self.drive_forward(Globals.FAST)
            i = self.angleRelative(Globals.red_bots[0].x, Globals.red_bots[0].y)
            if i < 0 or i > 40:
                self.turn_towards(Globals.red_bots[0].x, Globals.red_bots[0].y, Globals.FAST)
        else:
            print("PASS, RED4 attackFLAG()")

    def jailedf(self):
        # todo - if jailbroken
        Globals.red_bots[0].bot4ready = False
        if not self.jailed:
            self.curr_state = STATE.HOME
    
    def gohome(self):
        self.curr_state = STATE.WAIT
    
    """
    Helper Functions
    """     
    def evadeBots(self):
        closest_enemy, dist = self.closest_enemy_to_self(True)
        angle=self.angleRelative(closest_enemy.x,closest_enemy.y)
        if angle<0:
            self.turn_right(Globals.FAST)
        else:
            self.turn_left(Globals.FAST)
        # Driving forward
        self.drive_forward(Globals.FAST)

    def attack(self):
        bot, dista = self.closest_enemy_to_flag()
        print(dista, bot)
        # todo - attack bots
        if dista <= 200 and bot.x > 650:
            if dista < 200:
                i = self.angleRelative(bot.x + 30, bot.y)
                print(i)
                if i < 0 or i > 40:
                    self.turn_towards(bot.x + 30, bot.y, Globals.FAST)
                else:
                    self.drive_forward(Globals.FAST)
        elif dista > 300:
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

    def closest_enemy_to_enemyflag(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         Globals.red_flag.x, Globals.red_flag.y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         Globals.red_flag.x, Globals.red_flag.y)

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
