from GameFrame import Globals
from GameFrame.GenericBot import GenericBot
import GameFrame.RedBot
import GameFrame.BlueBot

class BlueBot(GenericBot):
    def __init__(self, room, x, y):
        self.COLOUR = Globals.BLUE_COLOUR
        self.set_colour_properties()
        GenericBot.__init__(self, room, x, y)

    def set_colour_properties(self):
        self.FLAG_TO_STEAL_WINNER = Globals.BLUE_FLAG_WINNER
        self.FLAG_TO_STEAL = Globals.blue_flag
        self.START_DIRECTION = -90
        self.MY_TEAM_BOTS = Globals.blue_bots
        self.JAIL_POSITION = (Globals.GAME_AREA_WIDTH_MIN + 25, Globals.GAME_AREA_HEIGHT_MIN + 25) #todo this could be an object for coords instead of a a tuple
        self.IMAGE = 'bot_blue.png'
        self.FLAG_NAME = 'BlueFlag'
        self.COLOUR_STRING = 'Blue'
        self.OTHER_TEAM_BOT_OBJECT = GameFrame.RedBot
        self.MY_TEAM_BOT_OBJECT = GameFrame.BlueBot

    # Helper method to set the global flag x and y depending on what colour the bot is
    def set_flag_position(self, x, y):
        Globals.blue_flag.x = x
        Globals.blue_flag.y = y
    
    #Helper method to get the global flag x and y depending on what colour the bot is
    def get_flag(self):
        return Globals.blue_flag
        
    #Helper set the flag heigh
    def set_local_flag_height(self):
        self.FLAG_HEIGHT = Globals.blue_flag.rect.height

    #Helper method to add to the global scores of each team
    def add_points_close_to_flag(self, points):
        Globals.blue_enemy_side_time += points