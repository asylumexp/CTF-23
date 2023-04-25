import os


class Globals:
    
    running = True
    FRAMES_PER_SECOND = 30

    # Constants for game logic 
    RED_COLOUR = 1
    BLUE_COLOUR = 2
    RED_FLAG_WINNER = 1
    BLUE_FLAG_WINNER = 2

    # Team names to be displayed during match and at end screen
    red_team_name = "Team Uno"
    blue_team_name = "Team Two"
    # Team Logos to be displayed during match
    red_team_logo = os.path.join("teamLogos", "Team1.png")
    blue_team_logo = os.path.join("teamLogos", "Team2.png")

    # Size of game screen
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # Bounding dimensions for the areas bots can move
    GAME_AREA_WIDTH_MIN = 32
    GAME_AREA_HEIGHT_MIN = 64
    GAME_AREA_WIDTH_MAX= SCREEN_WIDTH - GAME_AREA_WIDTH_MIN
    GAME_AREA_HEIGHT_MAX = SCREEN_HEIGHT - GAME_AREA_HEIGHT_MIN

    SCORE = 0

    # - Set the starting number of lives - #
    LIVES = 3

    # - Set the Window display name - #
    window_name = 'GF Capture the Flag'

    # - Set the order of the rooms - #
    levels = ["Arena", "EndScreen"]

    background_music = 0

    # - Winner Text - #
    winner = ' '

    # - Set the starting level - #
    start_level = 0

    # - Set this number to the level you want to jump to when the game ends - #
    end_game_level = 1

    # - Change variable to True to exit the program - #
    exiting = False

    # bot lists
    red_bots = []
    blue_bots = []

    # Flags
    red_flag = 0
    blue_flag = 0

    # Speeds
    SLOW = 2
    MEDIUM = 5
    FAST = 8

    # Direction
    LEFT = 0
    RIGHT = 1

    # Time in opposition half
    red_enemy_side_time = 0
    blue_enemy_side_time = 0

