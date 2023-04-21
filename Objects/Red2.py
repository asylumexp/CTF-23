from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 0
    ATTACK = 1
    JAILBREAK = 2
    RETURN = 3

class Red2(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.RETURN

    def tick(self):
        # Lame declaring outside init becuz of weird glitch with gameframe
        self.psuedoflagx=Globals.blue_flag.x-250
        if self.x < 660:
            self.curr_state == STATE.RETURN
        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.JAILBREAK:
            self.jailbreak()
        elif self.curr_state == STATE.RETURN:
            self.return_home()
        else:
            self.curr_state = STATE.WAIT

    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
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

    def attack(self):
        bot, distance = self.closest_enemy_to_flag()
        angle = self.angleRelative(bot.x,bot.y)
        self.turn_towards(bot.x+20, bot.y, Globals.FAST)
        if distance < 200 and angle < 70:
            self.drive_forward(Globals.FAST)
        if distance > 200:
            self.curr_state = STATE.WAIT

    def jailbreak(self):
        bot_jailed = False
        for team_bot in Globals.red_bots:
            if team_bot.jailed:
                bot_jailed = True
                break
        if not bot_jailed:
            self.curr_state = STATE.RETURN
        else:
            angle = self.angleRelative(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
            self.turn_towards(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT, Globals.FAST)
            if angle <120:
                self.drive_forward(Globals.FAST)

    def return_home(self):
        #if self.x <= self.psuedoflagx-40 or self.x >= self.psuedoflagx-50:
            #self.turn_towards(self.psuedoflagx-40, Globals.blue_flag.y, Globals.FAST)
            #self.drive_forward(Globals.FAST)
        if self.point_to_point_distance(self.x, self.y, self.psuedoflagx, Globals.blue_flag.y) > 30:
            self.turn_towards(self.psuedoflagx, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = STATE.WAIT

    def closest_enemy_to_flag(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest_bot.x, closest_bot.y,
                                                         self.psuedoflagx, Globals.blue_flag.y)
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(curr_bot.x, curr_bot.y,
                                                         self.psuedoflagx, Globals.blue_flag.y)
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance

    def angleRelative(self, x, y):
        angle = self.NormalizedAngle(x, y)
        diffangle = min(abs(self.angle-angle), 360-abs(self.angle-angle))
        return diffangle

    def NormalizedAngle(self,x,y):
        angle = self.get_rotation_to_coordinate(x,y)
        if angle < 0: angle += 360
        return angle
