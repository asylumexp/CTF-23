from GameFrame import BlueBot, Globals
from enum import Enum

class STATE(Enum):
    MISSOURI = 1  # * Strike state
    NORTH_CAROLINA = 2  # * Move to area state
    BALTIMORE = 3  # * Bait state
    BAIT_TRUE = 4  # * Prepare bait state
    JAIL = 5  # * Jail state
    JAILBREAK = 6 # * Jail Break State



class Blue5(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.curr_state = STATE.NORTH_CAROLINA
        try:
            self.set_image("Images/b5.png", 25, 25)
        except FileNotFoundError:
            print("hello this is me making a error checking for the set image we used images in our testing so we actually knew which bot was which if youre seeing this that means we again forgot to remove the set image for red5 which is awkward gotta say so bye have fun doing the competition.")

    def tick(self):
        # * States
        if self.curr_state == STATE.NORTH_CAROLINA:
            Globals.blue_bots[2].bait_bot_prepare(self, 650, 75, STATE.BAIT_TRUE)
        elif self.curr_state == STATE.MISSOURI:
            Globals.blue_bots[2].general_bot_attack(self, STATE.NORTH_CAROLINA)
        elif self.curr_state == STATE.BAIT_TRUE:
            Globals.blue_bots[2].bait_bot_wait(self, STATE.BALTIMORE)
        elif self.curr_state == STATE.BALTIMORE:
            Globals.blue_bots[2].bait_bot_bait(self, STATE.JAIL)
        elif self.curr_state == STATE.JAIL:
            Globals.blue_bots[2].general_bot_jailed(self, STATE.MISSOURI)
        elif self.curr_state == STATE.JAILBREAK:
            Globals.blue_bots[2].jailbreak(self, STATE.JAILBREAK)
        else:
            self.curr_state = STATE.NORTH_CAROLINA





'''class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    FLAG = 3
    PREPARE = 4
    BAIT = 5
    JAIL = 6
    HOME = 7


class Blue5(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.curr_state = STATE.WAIT
        self.set_image("Images/b5.png", 25, 25)

    def tick(self):
        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
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
        # Stay and or move close to the top border
        # todo Check for enemies
        if distance < 250:
            self.curr_state = STATE.ATTACK
        # todo Wait for Bait
        if self.x <= 594 or self.x >= 606:
            self.turn_towards(600, 600, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = STATE.PREPARE

    def prepare(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.curr_state = STATE.ATTACK
        self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
        Globals.blue_bots[0].bot5ready = True
        if Globals.blue_bots[0].bot4ready and Globals.blue_bots[0].bot3ready:
            self.curr_state = STATE.BAIT

    def bait(self):
        self.prev_state = STATE.BAIT
        bot, distance = self.closest_enemy_to_self(True)
        angle = abs(self.angleRelative(bot.x, bot.y))
        # ? move across border, evading enemies
        if self.x <= 50 and self.y < 100:
            self.jailedf()
        elif angle < 90 and distance < 200 and not self.has_flag:
            self.evadeBots()
        elif not self.has_flag:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        elif self.has_flag:
            i = self.angleRelative(Globals.blue_bots[0].x, Globals.blue_bots[0].y)
            if i < 0 or i > 40:
                self.turn_towards(
                    Globals.blue_bots[0].x, Globals.blue_bots[0].y, Globals.FAST
                )
            self.drive_forward(Globals.FAST)
        else:
            self.attackFLAG()

    def attackFLAG(self):
        # * If tagged:
        if self.jailed:
            self.curr_state = STATE.JAIL
        # todo - evade enemies
        # ? self.evadeBots()
        # todo - move to flag
        # todo - return with flag

    def jailedf(self):
        # todo - if jailbroken
        self.curr_state == STATE.JAIL
        Globals.blue_bots[0].bot5ready = False
        if not self.jailed:
            self.curr_state = STATE.HOME

    def gohome(self):
        # todo - move to upper position
        self.curr_state = STATE.WAIT

    def attack(self):
        bot, dista = self.closest_enemy_to_flag()
        print(dista, bot)
        # todo - attack bots
        if dista <= 200 and bot.x < 650:
            if dista < 200 and dista > 100:
                i = self.angleRelative(bot.x + 30, bot.y)
                print(i)
                if i < 0 or i > 40:
                    self.turn_towards(bot.x + 30, bot.y, Globals.FAST)
                else:
                    self.drive_forward(Globals.FAST)
            elif dista < 100:
                self.turn_towards(bot.x + 30, bot.y, Globals.FAST)
                self.drive_forward(Globals.FAST)
        elif dista > 300:
            self.curr_state = STATE.WAIT
        # todo - return to previous function
        pass

    """
    Helper Functions
    """

    # * Evade bots
    def evadeBots(self):
        closest_enemy, dist = self.closest_enemy_to_self(True)
        if self.angleRelative(closest_enemy.x, closest_enemy.y) < 0:
            self.turn_right(Globals.FAST)
        else:
            self.turn_left(Globals.FAST)
        # Driving forward
        self.drive_forward(Globals.FAST)

    # * Get opposite direction from self, from winner 2020 code
    def oppositeDirection(self):
        closest_bot, dist = self.closest_enemy_to_self(True)
        pointX = self.x - closest_bot.x
        pointY = self.y - closest_bot.y
        return pointX, pointY

    def attack(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.turn_towards(bot.x, bot.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = STATE.WAIT

    def closest_enemy_to_flag(self):
        closest_bot = Globals.red_bots[0]
        shortest_distance = self.point_to_point_distance(
            closest_bot.x, closest_bot.y, Globals.red_flag.x, Globals.red_flag.y
        )
        for curr_bot in Globals.red_bots:
            curr_bot_dist = self.point_to_point_distance(
                curr_bot.x, curr_bot.y, Globals.red_flag.x, Globals.red_flag.y
            )

            if curr_bot_dist < shortest_distance:
                shortest_distance = curr_bot_dist
                closest_bot = curr_bot

        return closest_bot, shortest_distance

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
            # * check enemy distance from self to bot from loop
            if curr_bot_dist < shortest_distance:
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
        return angle'''
