from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    MISSOURI = 1  # * Strike state
    NORTH_CAROLINA = 2  # * Move to area state
    BALTIMORE = 3  # * Bait state
    BAIT_TRUE = 4  # * Prepare bait state
    JAIL = 5  # * Jail state
    JAILBREAK = 6 # * Jail Break State
    FLAGRETURN = 7


class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.NORTH_CAROLINA
        try:
            self.set_image("Images/RED5.png", 25, 25)
        except FileNotFoundError:
            print("hello this is me making a error checking for the set image we used images in our testing so we actually knew which bot was which if youre seeing this that means we again forgot to remove the set image for red5 which is awkward gotta say so bye have fun doing the competition.")

    def tick(self):
        # * States
        if self.curr_state == STATE.NORTH_CAROLINA:
            Globals.red_bots[2].bait_bot_prepare(self, 650, 75, STATE.BAIT_TRUE)
        elif self.curr_state == STATE.MISSOURI:
            Globals.red_bots[2].general_bot_attack(self, STATE.NORTH_CAROLINA)
        elif self.curr_state == STATE.BAIT_TRUE:
            Globals.red_bots[2].bait_bot_wait(self, STATE.BALTIMORE)
        elif self.curr_state == STATE.BALTIMORE:
            Globals.red_bots[2].bait_bot_bait(self, STATE.JAIL)
        elif self.curr_state == STATE.JAIL:
            Globals.red_bots[2].general_bot_jailed(self, STATE.MISSOURI)
        elif self.curr_state == STATE.JAILBREAK:
            Globals.red_bots[2].jailbreak(self, STATE.JAILBREAK)
        elif self.curr_state == STATE.FLAGRETURN:
            self.flagreturn()
        else:
            self.curr_state = STATE.NORTH_CAROLINA


    def bait_bot_prepare(self: RedBot, bait_position_x: int, bait_position_y: int, wait_state: STATE):
        bot, distance = Globals.red_bots[2].closest_enemy_to_flag()
        if self.x <= bait_position_x - 6 or self.x >= bait_position_x + 6:
            self.turn_towards(bait_position_x, bait_position_y, Globals.FAST)
            self.drive_forward(Globals.FAST)
            if Globals.red_bots[4].curr_state == STATE.JAILBREAK:
                self.curr_state = STATE.FLAGRETURN 
        else:
            self.curr_state = wait_state


    def flagreturn(self):
        bot, distance = self.closest_enemy_to_flag()
        flagAngle = abs(self.angleRelative(Globals.blue_flag.x, Globals.blue_flag.y))
        if distance < 350:
            self.curr_state = STATE.MISSOURI
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
            self.curr_state = STATE.NORTH_CAROLINA
