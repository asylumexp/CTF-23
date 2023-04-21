from GameFrame import Globals
from GameFrame.GenericBot import GenericBot
import GameFrame.RedBot
import GameFrame.BlueBot

class RedBot(GenericBot):
    def __init__(self, room, x, y):
        self.COLOUR = Globals.RED_COLOUR
        self.set_colour_properties()
        GenericBot.__init__(self, room, x, y)

    def set_colour_properties(self):
        self.FLAG_TO_STEAL_WINNER = Globals.RED_FLAG_WINNER
        self.FLAG_TO_STEAL = Globals.red_flag
        self.START_DIRECTION = 90
        self.MY_TEAM_BOTS = Globals.red_bots
        self.JAIL_POSITION = (Globals.GAME_AREA_WIDTH_MAX - 25, Globals.GAME_AREA_HEIGHT_MAX - 25 )
        self.IMAGE = 'bot_red.png'
        self.FLAG_NAME = 'RedFlag'
        self.COLOUR_STRING = 'Red'
        self.OTHER_TEAM_BOT_OBJECT = GameFrame.BlueBot
        self.MY_TEAM_BOT_OBJECT = GameFrame.RedBot
    
    # Helper method to set the global flag x and y depending on what colour the bot is
    def set_flag_position(self, x, y):
        Globals.red_flag.x = x
        Globals.red_flag.y = y
    
    #Helper method to get the global flag x and y depending on what colour the bot is
    def get_flag(self):
        return Globals.red_flag
        
    #Helper set the flag heigh
    def set_local_flag_height(self):
        self.FLAG_HEIGHT = Globals.red_flag.rect.height

    #Helper method to add to the global scores of each team
    def add_points_close_to_flag(self, points):
        Globals.red_enemy_side_time += points