from GameFrame import RedBot, Globals
from enum import Enum


# TEST
# Work
class STATE(Enum):
    CHILL = 1
    STRIKE = 2
    FLAGRETURN = 3
    JAILBREAK = 4


class Red1(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.FLAGRETURN
        self.bot3ready = False
        self.bot4ready = False
        self.bot5ready = False
        try:
            self.set_image("Images/r1.png", 25, 25)
        except FileNotFoundError:
            print("hello this is me making a error checking for the set image we used images in our testing so we actually knew which bot was which if youre seeing this that means we again forgot to remove the set image for red1 which is awkward gotta say so bye have fun doing the competition.")


    def tick(self):
        if self.curr_state == STATE.FLAGRETURN:
            self.flagreturn()
        elif self.curr_state == STATE.CHILL:
            self.wait()
        elif self.curr_state == STATE.STRIKE:
            self.STRIKE()
        elif self.curr_state == STATE.JAILBREAK:
            self.jailbreak()
        else:
            self.curr_state = STATE.CHILL

    def flagreturn(self):
        bot, distance = self.closest_enemy_to_flag()
        flagAngle = abs(self.angleRelative(Globals.blue_flag.x, Globals.blue_flag.y))
        if distance < 350:
            self.curr_state = STATE.STRIKE
        elif (
            self.point_to_point_distance(
                self.x, self.y, Globals.blue_flag.x, Globals.blue_flag.y
            )
            > 20
        ):
            if flagAngle < 80:
                self.turn_towards(
                    Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST
                )
                self.drive_forward(Globals.FAST)
            else:
                self.turn_towards(
                    Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST
                )
        else:
            self.curr_state = STATE.CHILL

    def jailbreak(self):
        bot_jailed = False
        if Globals.red_bots[1].jailed:
            bot_jailed = True
        if not bot_jailed:
            self.curr_state = STATE.FLAGRETURN
        else:
            self.justincase()
            

    def justincase(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 300:
            self.curr_state == STATE.FLAGRETURN
        else:
            angle = self.angleRelative(Globals.SCREEN_WIDTH - 75, Globals.SCREEN_HEIGHT - 100)
            self.turn_towards(Globals.SCREEN_WIDTH - 75, Globals.SCREEN_HEIGHT - 100, Globals.FAST)
            if angle < 120:
                self.drive_forward(Globals.FAST)
                
    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        self.turn_towards(bot.x, bot.y, Globals.FAST)
        if distance < 175:
            self.curr_state = STATE.STRIKE
        else:
            bot_jailed = False
            for team_bot in Globals.red_bots:
                if team_bot.jailed:
                    bot_jailed = True
                    break
            if bot_jailed:
                self.curr_state = STATE.JAILBREAK

    def STRIKE(self):
        bot, distance = self.closest_enemy_to_flag()
        angle = abs(self.angleRelative(bot.x, bot.y))
        self.turn_towards(bot.x, bot.y, Globals.FAST)
        if distance < 125 and angle < 70:
            self.drive_forward(Globals.FAST)
        if distance > 125:
            s, bot1 = self.Single(350)
            if s:
                self.turn_towards(bot1.x, bot1.y, Globals.FAST)
                if angle < 70:
                    self.drive_forward(Globals.FAST)
            else:
                self.curr_state = STATE.FLAGRETURN

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

    def Single(self, dist):
        num = 0
        bot = Globals.blue_bots[0]
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, Globals.blue_flag.x, Globals.blue_flag.y
            )
            if curr_bot_dist < dist:
                num += 1
                bot = curr_bot
        if num == 1:
            return True, bot
        else:
            return False, bot
