from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    ATTACK = 1  # * Strike state
    BAIT_PREPARE = 2  # * Move to area state
    BAIT_BAIT = 3  # * Bait state
    BAIT_WAIT = 4  # * Prepare bait state
    JAIL = 5  # * Jail state
    JAILBREAK = 6  # * Jail Break state


class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.NORTH_CAROLINA
        self.priority = Priority_List(
            [STATE.ATTACK, STATE.BAIT_PREPARE, STATE.BAIT_BAIT, STATE.BAIT_WAIT, STATE.JAILBREAK], [2, 3, 4, 5, 1])
        try:
            self.set_image("Images/RED5.png", 25, 25)
        except FileNotFoundError:
            print("hello this is me making a error checking for the set image we used images in our testing so we actually knew which bot was which if youre seeing this that means we again forgot to remove the set image for red5 which is awkward gotta say so bye have fun doing the competition.")

    def tick(self):
        # * States
        try:
            val, state = self.priority.highestValue()
            if val != -1 or val != False:
                self.curr_state = state
        finally:
            if self.curr_state == STATE.BAIT_PREPARE:
                Globals.red_bots[2].bait_bot_prepare(
                    self, 650, 75, STATE.BAIT_TRUE)
            elif self.curr_state == STATE.ATTACK:
                Globals.red_bots[2].general_bot_attack(
                    self, STATE.NORTH_CAROLINA)
            elif self.curr_state == STATE.BAIT_WAIT:
                Globals.red_bots[2].bait_bot_wait(self, STATE.BALTIMORE)
            elif self.curr_state == STATE.BAIT_BAIT:
                Globals.red_bots[2].bait_bot_bait(self, STATE.JAIL)
            elif self.curr_state == STATE.JAIL:
                Globals.red_bots[2].general_bot_jailed(self, STATE.MISSOURI)
            else:
                self.curr_state = STATE.NORTH_CAROLINA


class Priority_List(object):
    def __init__(self, listOfStates: list, listOfTheirValues: list):
        self.queue = {}
        num = 0
        for i in listOfStates:
            print(num, i)
            self.queue[i] = listOfTheirValues[num]
            num += 1

    # * Checking if list is empty
    def isEmpty(self):
        return False if not self.queue else True

    # * Find the highest value state
    def highestValue(self):
        try:
            highestNum = -1
            highestState = STATE
            for key in self.queue:
                if self.queue[key] > highestNum:
                    highestNum = self.queue[key]
                    highestState = key
            return highestNum, highestState  # ! Bad if it equals -1
        except Exception:  # ! Fix so that its using the specific error
            return False, STATE

    # inserting states into list
    def insert(self, State: STATE, priority=0):
        self.queue[State] = priority
