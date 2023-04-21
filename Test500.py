#!/usr/bin/python3

import sys
import pygame
from GameFrame import Globals
Globals.FRAMES_PER_SECOND = 100000


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.font.init()

pygame.display.set_caption(Globals.window_name)
window_size = (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
screen = pygame.display.set_mode(window_size,
                                pygame.DOUBLEBUF, 32)

bluewins=0;
redwins=0;

numoftests=50

for i in range(numoftests):
    print(Globals.winner)
    if Globals.winner=="Red": 
        redwins +=1
    Globals.SCORE=0
    Globals.background_music =0
    Globals.LIVES=3
    Globals.red_bots=[]
    Globals.blue_bots=[]
    Globals.red_enemy_side_time=0
    Globals.blue_enemy_side_time=0
    Globals.red_flag=0
    Globals.blue_flag=0
    Globals.winner=' '

    Globals.next_level = Globals.start_level
    levels = Globals.levels
    

    # - Main Game Loop. Steps through the levels defined in levels[] - #
    while Globals.running:

        curr_level = Globals.next_level
        Globals.next_level += 1
        Globals.next_level %= len(levels)
        mod_name = "Rooms.{}".format(levels[curr_level])
        mod = __import__(mod_name)
        class_name = getattr(mod, levels[curr_level])
        room = class_name(screen)
        exit_val = room.run()

        if exit_val is True or Globals.running is False:
            # print(Globals.winner)
            # if Globals.winner=="Red": 
            #     redwins +=1
            Globals.next_level = Globals.end_game_level

            if len(levels) == 1:
                break

        if Globals.exiting:
            # print(Globals.winner)
            # if Globals.winner=="Red":
            #     redwins+=1
            break

print(f"""red wins: {redwins} win% = {redwins/100}%
blue wins: {numoftests-redwins} win% = {(numoftests-redwins)/100}%"""
)