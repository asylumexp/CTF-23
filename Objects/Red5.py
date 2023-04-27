from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    MISSOURI = 1  # * Strike state
    NORTH_CAROLINA = 2  # * Move to area state
    BALTIMORE = 3  # * Bait state
    BAIT_TRUE = 4  # * Prepare bait state
    JAIL = 5  # * Jail state
    JAILBREAK = 6 # * Jail Break state


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

#Priority List for changing priority of states
class Priority_List(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return "".join([str(queue) for queue in self.queues])
    
    #Checking if list is empty
    def isEmpty(self):
        return len(self.queues) == 0
    
    #inserting states into list
    def insert(self, State):
        self.queue.append(State)

    #Setting the priority of the state
    def delete(self):
        try:
            max_val = 0
            for i in range(len(self.queues)):
                if self.queues[i] > self.queue[max_val]:
                    max_val = i
            item = self.queue[max_val]
            del self.queue[max_val]
            return item
        except IndexError:
            print("error")
            exit()

if __name__ == "__main__":
    MISSOURI = 2
    NORTH_CAROLINA = 3
    BALTIMORE = 4
    BAIT_TRUE = 5
    JAILBREAK = 1
    if Globals.red_bots[3].x >= 1100 and Globals.red_bots[3].y >= 600:
        JAILBREAK =+ 5
        
    PriorityQueue = Priority_List()
    PriorityQueue.insert(MISSOURI)
    PriorityQueue.insert(NORTH_CAROLINA)
    PriorityQueue.insert(BALTIMORE)
    PriorityQueue.insert(BAIT_TRUE)
    print(PriorityQueue)

    def Priority_State_Change(self):
        if PriorityQueue[0] == MISSOURI:
            Globals.red_bots[2].general_bot_attack(self, STATE.NORTH_CAROLINA)
        if PriorityQueue[0] == NORTH_CAROLINA:
            Globals.red_bots[2].bait_bot_prepare(self, 650, 75, STATE.BAIT_TRUE)
        if PriorityQueue[0] == BALTIMORE:
            Globals.red_bots[2].bait_bot_bait(self, STATE.JAIL)
        if PriorityQueue[0] == BAIT_TRUE:
            Globals.red_bots[2].bait_bot_wait(self, STATE.BALTIMORE)
        if PriorityQueue[0] == JAILBREAK:
            Globals.red_bots[2].jailbreak(self, STATE.JAILBREAK)

        while not PriorityQueue.isEmpty():
            print(PriorityQueue.delete())


