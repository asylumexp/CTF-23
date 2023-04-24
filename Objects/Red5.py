from GameFrame import RedBot, Globals
from enum import Enum


class STATE(Enum):
    MISSOURI = 1  # * Strike state
    NORTH_CAROLINA = 2  # * Move to area state
    BALTIMORE = 3  # * Bait state
    BAIT_TRUE = 4  # * Prepare bait state
    JAIL = 5  # * Jail state


class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.curr_state = STATE.NORTH_CAROLINA
        self.set_image("Images/RED5.png", 25, 25)

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

    # *evade function
    #not me not so subtley using the frame stacking bug
    def evadeBots(self):
        closest_enemy, dist = self.closest_enemy_to_self(True)
        angle = self.angleRelative(closest_enemy.x, closest_enemy.y)
        if angle < 0:
            self.turn_right(Globals.FAST)
            self.turn_right(Globals.MEDIUM)
            self.turn_right(Globals.SLOW)
            self.drive_forward(Globals.FAST)
            self.drive_forward(Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            self.turn_left(Globals.FAST)
            self.turn_left(Globals.MEDIUM)
            self.turn_left(Globals.SLOW)
            self.drive_forward(Globals.FAST)
            self.drive_forward(Globals.FAST)
            self.drive_forward(Globals.FAST)
        # Driving forward
        self.drive_forward(Globals.FAST)

    def EnemySpeedCheck(self):
        pass
        #goal is to check the closest enemy bots speed and so if its fast you'd turn and move slow so hopefully they move past you, and if they're medium or slow you move and turn fast, i just forgot how to check this, i was thinking something like "print blue bot speed, this blue bot speed = bspeed, if bspeed = Globals.SLOW: self speed would be yk fast. obv turning speed and movement speed oulwd be diifernet, so like. "blue turning speed = btspeed = Globals.SLOW" hopefully u undersatnd. 
