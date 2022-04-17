import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.game.display.fill((0, 0, 0))
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100
        pygame.mixer.init()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.game.open_main_menu = True
        self.state = "start"
        self.start_x, self.start_y = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30
        self.continue_x, self.continue_y = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50
        self.options_x, self.options_y = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70
        self.credits_x, self.credits_y = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 90
        self.quit_x, self.quit_y = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 120
        self.HS_x, self.HS_y = self.game.DISPLAY_W / 2, self.game.DISPLAY_H - 30
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)

    def draw_cursor(self):
        self.game.write_txt("*", 20, self.cursor_rect.x, self.cursor_rect.y)

    def draw_main_menu(self):

        self.game.display.fill((0, 0, 0))
        self.game.write_txt("Main menu", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
        self.game.write_txt("start", 20, self.start_x, self.start_y)
        self.game.write_txt("continue", 20, self.continue_x, self.continue_y)
        self.game.write_txt("options", 20, self.options_x, self.options_y)
        self.game.write_txt("credits", 20, self.credits_x, self.credits_y)
        self.game.write_txt("quit", 20, self.quit_x, self.quit_y)
        self.game.write_txt(f"Highscore: {self.game.high_score}", 20, self.HS_x, self.HS_y)
        self.draw_cursor()

    def move_cursor(self):

        if self.game.KEY_DOWN:
            if self.state == "start":
                self.cursor_rect.midtop = (self.continue_x + self.offset, self.continue_y)
                self.state = "continue"

            elif self.state == "continue":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "options"

            elif self.state == "options":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "credits"

            elif self.state == "credits":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "quit"

            elif self.state == "quit":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "start"

        elif self.game.KEY_UP:

            if self.state == "start":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "quit"

            elif self.state == "continue":
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = "start"

            elif self.state == "options":
                self.cursor_rect.midtop = (self.continue_x + self.offset, self.continue_y)
                self.state = "continue"

            elif self.state == "credits":
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = "options"

            elif self.state == "quit":
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = "credits"

        if self.game.KEY_RETURN:
            if self.state == "start":
                self.game.new_game()
                self.game.run_main_menu = False
                self.game.playing = True
                self.game.bg_music = 0
                self.game.play_music("background_theme", self.game.bg_music)
            if self.state == "quit":
                self.game.run_main_menu = False
                self.game.playing = False
                self.game.running = False

            if self.state == "continue":
                if self.game.new:
                    self.game.run_main_menu = False
                    self.game.playing = True
                    pygame.mixer.music.pause()
                    print(self.game.bg_music)
                    self.game.play_music("background_theme",self.game.bg_music)

    def clear_screen(self):
        self.game.display.fill((0, 0, 0))

    def run(self):
        self.game.run_main_menu = True
        self.game.play_music("main_menu_music", self.game.menu_music)
        while self.game.run_main_menu:
            self.game.check_events()
            self.move_cursor()
            self.draw_main_menu()
            self.game.draw_display()
