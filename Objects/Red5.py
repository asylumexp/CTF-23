from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    MISSOURI = 1  # * Strike state
    NORTH_CAROLINA = 2  # * Move to area state
    BALTIMORE = 3  # * Bait state
    BAIT_TRUE = 4  # * Prepare bait state
    JAIL = 5  # * Jail state
    JAILBREAK = 6 # * Jail Break State


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
        else:
            self.curr_state = STATE.NORTH_CAROLINA


    def Coreys_Dumb_Bot(self):
        if (Globals.red_bots[3].x >= 1100 and Globals.red_bots[3].y >= 600 ):
            Globals.red_bots[2].jailbreak(self, STATE.JAILBREAK)
