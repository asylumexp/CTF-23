from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    JAIL_BREAK = 3


class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)

        self.curr_state = STATE.WAIT

    def tick(self):

        if self.curr_state == STATE.WAIT:
            self.wait()
        elif self.curr_state == STATE.ATTACK:
            self.attack()
        elif self.curr_state == STATE.JAIL_BREAK:
            self.jailbreak()
        else:
            self.curr_state = STATE.WAIT

    def wait(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.curr_state = STATE.ATTACK
        else:
            bot_jailed = False
            for team_bot in Globals.red_bots:
                if team_bot.jailed:
                    bot_jailed = True
                    break
            if bot_jailed:
                self.curr_state = STATE.JAIL_BREAK

    def attack(self):
        bot, distance = self.closest_enemy_to_flag()
        if distance < 250:
            self.turn_towards(bot.x, bot.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.curr_state = STATE.WAIT

    def jailbreak(self):
        bot_jailed = False
        for team_bot in Globals.red_bots:
            if team_bot.jailed:
                bot_jailed = True
                break
        if not bot_jailed:
            self.curr_state = STATE.WAIT
        else:
            self.turn_towards(Globals.GAME_AREA_WIDTH_MAX - 36, Globals.GAME_AREA_HEIGHT_MAX - 40, Globals.FAST)
            self.drive_forward(Globals.FAST)

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
