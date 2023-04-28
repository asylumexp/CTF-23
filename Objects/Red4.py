from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    BAIT_PREPARE = 1
    ATTACK = 2
    BAIT_WAIT = 3
    BAIT_BAIT = 4
    JAIL = 5


class Red4(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.BAIT_PREPARE
        try:
            self.set_image("Images/r4.png", 25, 25)
        except FileNotFoundError:
            print("hello this is me making a error checking for the set image we used images in our testing so we actually knew which bot was which if youre seeing this that means we again forgot to remove the set image for red4 which is awkward gotta say so bye have fun doing the competition.")

    def tick(self):
        if self.curr_state == STATE.BAIT_PREPARE:
            Globals.red_bots[2].bait_bot_prepare(
                self, 650, 250, STATE.BAIT_WAIT)
        elif self.curr_state == STATE.ATTACK:
            Globals.red_bots[2].general_bot_attack(self, STATE.BAIT_PREPARE)
        elif self.curr_state == STATE.BAIT_WAIT:
            Globals.red_bots[2].bait_bot_wait(self, STATE.BAIT_BAIT)
        elif self.curr_state == STATE.BAIT_BAIT:
            Globals.red_bots[2].bait_bot_bait(self, STATE.JAIL)
        elif self.curr_state == STATE.JAIL:
            Globals.red_bots[2].general_bot_jailed(self, STATE.BAIT_PREPARE)
        else:
            self.curr_state = STATE.BAIT_PREPARE
