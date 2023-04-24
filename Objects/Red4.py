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
        self.set_image("Images/r4.png", 25, 25)

    def tick(self):
        if self.curr_state == STATE.WAIT:
            Globals.red_bots[2].bait_bot_prepare(self, 650, 250, STATE.PREPARE)
        elif self.curr_state == STATE.ATTACK:
            Globals.red_bots[2].general_bot_attack(self, STATE.WAIT)
        elif self.curr_state == STATE.PREPARE:
            Globals.red_bots[2].bait_bot_wait(self, STATE.BAIT)
        elif self.curr_state == STATE.BAIT:
            Globals.red_bots[2].bait_bot_bait(self, STATE.JAIL)
        elif self.curr_state == STATE.JAIL:
            Globals.red_bots[2].general_bot_jailed(self, STATE.HOME)
        elif self.curr_state == STATE.HOME:
            Globals.red_bots[2].general_bot_return(self, STATE.WAIT)
        else:
            self.curr_state = STATE.WAIT