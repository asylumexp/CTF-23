from GameFrame import Level, TextObject, Globals


class EndScreen(Level):
    def __init__(self, screen):
        Level.__init__(self, screen)
        if Globals.winner == Globals.RED_FLAG_WINNER:
            winner = Globals.red_team_name
            colour = (255, 0, 0)
        elif Globals.winner == Globals.BLUE_FLAG_WINNER:
            winner = Globals.blue_team_name
            colour = (0, 0, 255)
        else:
            winner = 'Draw'
            colour = (255, 255, 255)

        winner_text = TextObject(self, Globals.SCREEN_WIDTH / 3, Globals.SCREEN_HEIGHT / 3 * 2, winner, 80)
        winner_text.colour = colour
        winner_text.update_text()
        winner_text.x = Globals.SCREEN_WIDTH / 2 - winner_text.width / 2
        self.add_room_object(winner_text)

        battle_text = TextObject(self, Globals.SCREEN_WIDTH / 3, Globals.SCREEN_HEIGHT / 3, 'Battle Winner', 80)
        battle_text.colour = colour
        battle_text.update_text()
        battle_text.x = Globals.SCREEN_WIDTH / 2 - battle_text.width / 2
        self.add_room_object(battle_text)

        Globals.background_music.stop()

        break_sound = self.load_sound('rock_breaking.ogg')
        self.applause = self.load_sound('applause.wav')
        break_sound.play()
        self.set_timer(60, self.applaud)

        self.set_timer(240, self.end_game)

    def applaud(self):
        self.applause.play()

    def end_game(self):
        # Append the result to the file 'results.txt'
        log_file = open('results.txt', 'a')
        if Globals.winner == Globals.RED_FLAG_WINNER:
            log_file.write("Red" + ' ')
        else:
            log_file.write("Blue" + ' ')
        
        self.running = False
        self.quitting = True
        Globals.exiting = True
        
        log_file.write("Red {} ".format(Globals.red_enemy_side_time))
        log_file.write("Blue {}\n".format(Globals.blue_enemy_side_time))
        
        log_file.close()
