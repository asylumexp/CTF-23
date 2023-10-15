from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    MISSOURI = 1  # * Strike state
    NORTH_CAROLINA = 2  # * Move to area state
    BALTIMORE = 3  # * Bait state
    BAIT_TRUE = 4  # * Prepare bait state
    JAIL = 5  # * Jail state
    JAILBREAK = 6  # * Jail Break State


class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = None
        

    def tick(self):
        if self.curr_state == STATE.NORTH_CAROLINA:
            Globals.red_bots[2].bait_bot_prepare(
                self, 650, 75, STATE.BAIT_TRUE)
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
        else:
            self.curr_state = STATE.NORTH_CAROLINA
