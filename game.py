import os

from scoreboard import *
import time
from apple import *
from pygame.locals import *
from menu import*
from snake import *
from os import path
from settings import*


import pygame

high_score_File = "Highscore.txt"

class Game:

    position = 50
    SIZE = 50

    def data_to_load(self):

        with open(HS_FILE, 'r+') as f:

            print(path.join(self.directory, HS_FILE))
            f.seek(0)
            if f.read() != "":
                f.seek(0)
                print(f.read())
                f.seek(0)
                self.high_score = int(f.read())
                print(f"high score is now: {self.high_score}")
            else:
                self.high_score = 0

    def __init__(self):
        pygame.init()

        self.running, self.playing, self.run_main_menu, self.new = False, False, False, False
        self.menu_music, self.bg_music = 0.000, 0.000
        self.DISPLAY_W, self.DISPLAY_H = 1000, 1000
        self.KEY_UP, self.KEY_DOWN, self.KEY_LEFT, self.KEY_RIGHT = False, False, False, False
        self.KEY_RETURN, self.KEY_ESCAPE = False, False
        self.font_name = pygame.font.get_default_font()
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.level_bg = []
        self.level_bg.append(pygame.image.load("resources/level1_bg.png.").convert())
        self.snake = Snake(self.display, 3, self.position, self.SIZE, 0)
        # self.snake.draw(self.display, self.snake.block, self.snake.rotation)
        self.apple = Apple(self.display, self.SIZE)
        self.apple.draw()
        self.scoreboard = Scoreboard(self.display, self.SIZE, self.DISPLAY_W)
        self.scoreboard.draw_score()
        self.directory = path.dirname(__file__)
        self.high_score = 0
        self.data_to_load()
        self.m_menu = MainMenu(self)
        pygame.mixer.init()



    def draw_display(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_events()


    def clear_screen(self):
        self.display.blit(self.level_bg[0], (0, 0))
        # self.display.fill((110, 110, 5))

    def write_txt(self, text, size, position_x, position_y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (position_x, position_y)
        self.display.blit(text_surface, text_rect)

    def speed_adjust(self):
        if self.snake.speed >= 0.1:
            if self.scoreboard.score_counter % 5.00 == 0.00:
                print("changing speed")
                self.snake.speed -= 0.05

    def play_sound(self, sound):

        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_music(self, music, position):
        pygame.mixer.music.load(f"resources/{music}.mp3")
        pygame.mixer.music.play(-1, position)

    def collision(self, x1, x2, y1, y2):
        if (x1 >= x2) and (x1 < x2 + self.SIZE):
            if (y1 >= y2) and (y1 < y2 + self.SIZE):
                return True

    def game_over(self):

        self.write_txt("GAME OVER", 40, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        self.write_txt(f"Score: {self.scoreboard.score_counter}", 40, self.DISPLAY_W/2, self.DISPLAY_H/2 + 40)

        if self.scoreboard.score_counter >= self.high_score:
            self.high_score = self.scoreboard.score_counter
            with open(HS_FILE, 'w+') as f:
                f.write(str(self.scoreboard.score_counter))
                self.write_txt("NEW HIGH SCORE!", 20, self.DISPLAY_W/2, self.DISPLAY_H/2 + 80)
        else:
            self.write_txt(f"High Score: {self.high_score}", 20, self.DISPLAY_W/2, self.DISPLAY_H/2 + 80)

        self.write_txt("press Escape to go back to main menu", 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2 + 160)

        self.draw_display()

        return True

    def new_game(self):
        self.new = True
        self.snake.reset_snake()
        self.apple.move()
        self.scoreboard.reset_score()
        self.menu_music, self.bg_music = 0.000, 0.000
        self.play_music("background_theme", self.bg_music)

    def pause_game(self):
        self.snake.keep_still()
        pygame.mixer.music.pause()

    def check_events(self):

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.KEY_ESCAPE = True
                    if self.playing:
                        self.playing = False
                        self.bg_music += (pygame.mixer.music.get_pos()/1000)
                        pygame.mixer.music.pause()
                    elif self.running and not self.playing:

                        if self.new:

                            self.run_main_menu = False
                            self.playing = True
                            pygame.mixer.music.pause()
                            print(self.bg_music)
                            self.play_music("background_theme", self.bg_music)

                if event.key == K_UP:
                    self.KEY_UP = True

                if event.key == K_DOWN:
                    self.KEY_DOWN = True

                if event.key == K_LEFT:
                    self.KEY_LEFT = True

                if event.key == K_RIGHT:
                    self.KEY_RIGHT = True

                if event.key == K_RETURN:
                    self.KEY_RETURN = True

            elif event.type == QUIT:
                self.playing, self.run_main_menu, self.running, self.new = False, False, False, False

    def reset_events(self):
        self.KEY_UP, self.KEY_DOWN, self.KEY_LEFT, self.KEY_RIGHT = False, False, False, False
        self.KEY_RETURN, self.KEY_ESCAPE = False, False

    def change_direction(self):
        if self.KEY_UP:
            if self.snake.x[1] == self.snake.x[0] and self.snake.y[1] == self.snake.y[0] - 50:
                pass
            elif self.snake.direction == "none":
                pass
            elif 0 >= self.snake.x[0] >= 0 + self.SIZE:
                pass
            elif 1000 <= self.snake.x[0] <= 1000 + self.SIZE:
                pass
            else:
                self.snake.move_up()

        if self.KEY_DOWN:

            if self.snake.x[1] == self.snake.x[0] and self.snake.y[1] == self.snake.y[0] + 50:

                pass
            elif self.snake.direction == "none":
                pass
            elif 0 >= self.snake.x[0] >= 0 + self.SIZE:
                pass
            elif 1000 <= self.snake.x[0] <= 1000 + self.SIZE:
                pass
            else:
                self.snake.move_down()

        if self.KEY_RIGHT:
            if self.snake.y[1] == self.snake.y[0] and self.snake.x[1] == self.snake.x[0] + 50:
                pass
            elif self.snake.direction == "none":
                pass
            elif 0 >= self.snake.y[0] >= 0 + self.SIZE:
                pass
            elif 1000 <= self.snake.y[0] <= 1000 + self.SIZE:
                pass

            else:
                self.snake.move_right()

        if self.KEY_LEFT:

            if self.snake.y[1] == self.snake.y[0] and self.snake.x[1] == self.snake.x[0] - 50:
                pass
            elif self.snake.direction == "none":
                pass
            elif 0 >= self.snake.y[0] >= 0 + self.SIZE:
                pass
            elif 1000 <= self.snake.y[0] <= 1000 + self.SIZE:
                pass
            else:
                self.snake.move_left()

    def update(self):
        self.clear_screen()
        self.check_events()
        # self.snake.draw(self.display, self.snake.block, self.snake.rotation)
        self.apple.draw()
        self.scoreboard.draw_score()

        if not self.snake.live:
            if not self.game_over():
                self.game_over()

        if self.snake.live:
            self.change_direction()
            self.collision_check()
            self.snake.walk()
            self.collision_check()


    def collision_check(self):

        # delete above
        if self.collision(self.snake.x[0], self.apple.x, self.snake.y[0], self.apple.y):
            if not self.snake.live:
                pass
            else:
                self.play_sound("eat_sound")
                self.apple.clear()
                self.apple.move()
                self.snake.eat = 0
                self.apple.draw()
                self.snake.draw_head(self.display, self.snake.block, self.snake.rotation)
                self.snake.increase_length()

                self.scoreboard.add_score()

                self.speed_adjust()

        for i in range(3, self.snake.length, 1):
            if self.collision(self.snake.x[0], self.snake.x[i], self.snake.y[0], self.snake.y[i]):
                self.game_over()
                self.snake.live = False
                self.pause_game()
                self.play_sound("loss")

    # main game-loop-------------------------------------------------------------------------------
    def run(self):
        self.running = True

        while self.running:
            self.m_menu.draw_main_menu()
            self.draw_display()
            self.m_menu.run()

            while self.playing:

                self.update()
                self.draw_display()
                time.sleep(self.snake.speed)
                self.reset_events()
