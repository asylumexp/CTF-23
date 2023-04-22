from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    MICHIGAN = 0  # * Wait state
    MISSOURI = 1  # * Strike state
    NORTH_CAROLINA = 2  # * Move to area state
    BALTIMORE = 3  # * Bait state
    BAIT_TRUE = 4  # * Prepare bait state
    JAIL = 5  # * Jail state


class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.MICHIGAN
        self.set_image("Images/RED5.png", 25, 25)

    def tick(self):
        # * States
        if self.curr_state == STATE.NORTH_CAROLINA:
            self.NORTH_CAROLINA()
        elif self.curr_state == STATE.MISSOURI:
            self.MISSOURI()
        elif self.curr_state == STATE.MICHIGAN:
            self.MICHIGAN()
        elif self.curr_state == STATE.BAIT_TRUE:
            self.BAIT_TRUE()
        elif self.curr_state == STATE.BALTIMORE:
            self.BALTIMORE()
        elif self.curr_state == STATE.JAIL:
            self.JAIL()
        else:
            self.curr_state = STATE.MICHIGAN

    # * Moving to prepare area
    def NORTH_CAROLINA(self):
        # * Drive until in position in upper region
        if self.x <= 644 or self.x >= 656:
            self.turn_towards(650, 75, Globals.FAST)
            self.drive_forward(Globals.FAST)
        # * If that the area, start the bait prepare
        else:
            self.curr_state = STATE.BAIT_TRUE

    # * Attack State
    def MISSOURI(self):
        # * Check for bot
        bot, distance = self.closest_enemy_to_bot()
        angle = self.angleRelative(bot.x, bot.y)
        self.turn_towards(bot.x, bot.y, Globals.SLOW)
        if distance < 100 and angle < 70:
            self.drive_forward(Globals.FAST)
        if distance > 100:
            self.curr_state = STATE.MICHIGAN

    # * Waiting for other bait bots
    def BAIT_TRUE(self):
        Globals.red_bots[0].bot5ready = True
        if Globals.red_bots[0].bot3ready and Globals.red_bots[0].bot4ready:
            self.curr_state = STATE.BALTIMORE

    #  * Checking for enemies
    def MICHIGAN(self):
        bot, distance = self.closest_enemy_to_bot()
        if distance < 250:
            self.curr_state = STATE.MISSOURI

        else:
            self.curr_state = STATE.NORTH_CAROLINA
   
    # * Bait state
    def BALTIMORE(self):
        bot, dist = self.closest_enemy_to_bot()
        ptpd = self.point_to_point_distance(self.x, self.y, bot.x, bot.y)
        angle = abs(self.angleRelative(bot.x, bot.y))
        if self.x >= 1100 and self.y >= 600:
            self.curr_state = STATE.JAIL
        elif angle < 60 and ptpd < 200 and not self.has_flag:
            self.evadeBots()
        elif not self.has_flag:
            self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            i = self.angleRelative(Globals.red_bots[0].x, Globals.red_bots[0].y)
            if i < 0 or i > 50:
                self.turn_towards(
                    Globals.red_bots[0].x, Globals.red_bots[0].y, Globals.FAST
                )
            self.drive_forward(Globals.FAST)
        else:
            print("PASS, RED5 BALTIMORE()")

    # * Jail state
    def JAIL(self):
        Globals.red_bots[0].bot5ready = False
        if not self.jailed:
            self.Acquitted()

    # ** Helper Functions **

    #*not in jail state
    def Acquitted(self):
        self.curr_state = STATE.MICHIGAN

    # *evade function
    #not me not so subtley using the frame stacking bug
    def evadeBots(self):
        closest_enemy, dist = self.closest_enemy_to_self(True)
        angle = self.angleRelative(closest_enemy.x, closest_enemy.y)
        if angle < 0:
            self.turn_right(Globals.FAST)
            self.turn_right(Globals.MEDIUM)
            self.turn_right(Globals.SLOW)
            self.drive_forward(Globals.FAST)
            self.drive_forward(Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.turn_left(Globals.FAST)
            self.turn_left(Globals.MEDIUM)
            self.turn_left(Globals.SLOW)
            self.drive_forward(Globals.FAST)
            self.drive_forward(Globals.FAST)
            self.drive_forward(Globals.FAST)
        # Driving forward
        self.drive_forward(Globals.FAST)

    # * get closest enemy to self
    def closest_enemy_to_bot(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, Globals.red_bots[4].x, Globals.red_bots[4].y
        )
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, Globals.red_bots[4].x, Globals.red_bots[4].y
            )
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance
    
    #*STUFF I STOLE FROM SAMS CODE sorry for caps mb bro
    def closest_enemy_to_self(self, ignore):
        # todo - make more efficient
        closest_bot = Globals.blue_bots[0]
        closer_bot = Globals.red_bots[0]
        shortest_distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, self.x, self.y
        )
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, self.x, self.y
            )
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

    # * Get closest enemy to the flag
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

    # * Relative angle calculation
    def angleRelative(self, x, y):
        angle = self.NormalizedAngle(x, y)
        diffangle = min(abs(self.angle - angle), 360 - abs(self.angle - angle))
        return diffangle

    # * normalised angle calculation
    def NormalizedAngle(self, x, y):
        angle = self.get_rotation_to_coordinate(x, y)
        if angle < 0:
            angle += 360
        return angle
    
    def EnemySpeedCheck(self):
        pass
        #goal is to check the closest enemy bots speed and so if its fast you'd turn and move slow so hopefully they move past you, and if they're medium or slow you move and turn fast, i just forgot how to check this, i was thinking something like "print blue bot speed, this blue bot speed = bspeed, if bspeed = Globals.SLOW: self speed would be yk fast. obv turning speed and movement speed oulwd be diifernet, so like. "blue turning speed = btspeed = Globals.SLOW" hopefully u undersatnd. 
