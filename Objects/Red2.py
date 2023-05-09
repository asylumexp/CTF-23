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
        try:
            self.set_image("Images/r2.png", 25, 25)
        except FileNotFoundError:
            print("hello this is me making a error checking for the set image we used images in our testing so we actually knew which bot was which if youre seeing this that means we again forgot to remove the set image for red2 which is awkward gotta say so bye have fun doing the competition.")


    def tick(self):
        # Lame declaring outside init becuz of weird glitch with gameframe
        self.psuedoflagx = Globals.blue_flag.x - 250
        print(f" Corey's Bot is in the state, {self.curr_state}")
        if self.x < 660:
            self.curr_state == STATE.RETURN
        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            Globals.red_bots[2].general_bot_attack(self, STATE.WAIT)
        elif self.curr_state == STATE.JAILBREAK:
            Globals.red_bots[2].jailbreak(self, STATE.JAILBREAK)
        elif self.curr_state == STATE.RETURN:
            Globals.red_bots[2].return_home(self, STATE.RETURN)
        else:
            self.curr_state = STATE.WAIT


    def wait(self):
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

    

    



    def closest_enemy_to_flag(self):
        closest_bot = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, self.psuedoflagx, Globals.blue_flag.y
        )
        for curr_bot in Globals.blue_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, self.psuedoflagx, Globals.blue_flag.y
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