from GameFrame import BlueBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 0
    ATTACK = 1
    JAILBREAK = 2
    RETURN = 3
    TESTING = 4


class Blue2(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.curr_state = STATE.RETURN
        try:
            self.set_image("Images/b2.png", 25, 25)
        except FileNotFoundError:
            print("hello this is me making a error checking for the set image we used images in our testing so we actually knew which bot was which if youre seeing this that means we again forgot to remove the set image for red2 which is awkward gotta say so bye have fun doing the competition.")

    def tick(self):
        # Lame declaring outside init becuz of weird glitch with gameframe
        print(f"corey's dumb blue bot is in {self.curr_state}")
        print(Globals.red_bots[1].x, Globals.red_bots[1].y)
        self.psuedoflagx = Globals.red_flag.x - 250
        if self.x < 660:
            self.curr_state == STATE.RETURN
        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.TESTING:
            self.testing()
        elif self.curr_state == STATE.JAILBREAK:
            self.jailbreak()
        elif self.curr_state == STATE.RETURN:
            self.return_home()
        else:
            self.curr_state = STATE.WAIT

    def testing(self):
        for i in range(1000):
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y)
            self.drive_forward(Globals.FAST)

    def wait(self):
        bot, distance = self.closest_enemy_to_self(True)
        if distance < 175:
            if self.x < 600:
                self.curr_state = STATE.RETURN
            else:
                self.curr_state = STATE.ATTACK
        else:
            bot_jailed = False
            for team_bot in Globals.blue_bots:
                if team_bot.jailed:
                    bot_jailed = True
                    break
            if bot_jailed:
                self.curr_state = STATE.JAILBREAK
        self.turn_towards(Globals.blue_flag.x + 200, 300)
        self.drive_forward(Globals.MEDIUM)
     

    def attack(self):
        bot, distance = self.closest_enemy_to_self(True)
        angle = self.angleRelative(bot.x, bot.y)
        self.turn_towards(bot.x + 20, bot.y, Globals.FAST)
        if distance < 200 and angle < 70:
            self.drive_forward(Globals.FAST)
        if distance > 200:
            self.curr_state = STATE.WAIT

    def jailbreak(self):
        bot_jailed = False
        if Globals.blue_bots[2].jailed:
            save_bot = Globals.blue_bots[2]
            bot_jailed = True
            if bot_jailed == True:
                self.turn_towards(save_bot.x + 20, save_bot.y - 20 , Globals.MEDIUM)
                self.drive_forward(Globals.FAST)
                bot_jailed = False
        elif Globals.blue_bots[3].jailed:
            save_bot = Globals.blue_bots[3]
            bot_jailed = True
            if bot_jailed == True:
                self.turn_towards(save_bot.x + 20, save_bot.y - 20 , Globals.MEDIUM)
                self.drive_forward(Globals.FAST)
                bot_jailed = False
        elif Globals.blue_bots[4].jailed:
            save_bot = Globals.blue_bots[4]
            bot_jailed = True
            if bot_jailed == True:
                self.turn_towards(save_bot.x + 20, save_bot.y - 20 , Globals.MEDIUM)
                self.drive_forward(Globals.FAST)
                bot_jailed = False
        if bot_jailed == False:
            self.curr_state = STATE.RETURN
        print(bot_jailed)

    def return_home(self):
        bob = True
        if bob == True:
            self.turn_towards(400,400, Globals.SLOW)
            bob = False
        else:
            self.curr_state = STATE.WAIT

    def closest_enemy_to_flag(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, self.psuedoflagx, Globals.red_flag.y
        )
        for curr_bot in Globals.red_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, self.psuedoflagx, Globals.red_flag.y
            )
            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance

    def angleRelative(self, x, y):
        angle = self.NormalizedAngle(x, y)
        diffangle = min(abs(self.angle - angle), 360 - abs(self.angle - angle))
        return diffangle

    def NormalizedAngle(self, x, y):
        angle = self.get_rotation_to_coordinate(x, y)
        if angle < 0:
            angle += 360
        return angle

    def closest_enemy_to_self(self, ignore):
        # todo - make more efficient
        closest_bot = Globals.red_bots[0]
        closer_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, self.x, self.y
        )
        for curr_bot in Globals.red_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, self.x, self.y
            )
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