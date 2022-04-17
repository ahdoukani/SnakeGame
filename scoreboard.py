import pygame

from game import*

class Scoreboard:
    def __init__(self, parent_screen, size, display_w):
        self.DISPLAY_W = display_w
        self.SIZE = size
        self.thousands = 0
        self.hundreds = 0
        self.tens = 0
        self.units = 0
        self.parent_screen = parent_screen
        self.score = [self.thousands, self.hundreds, self.tens, self.units]
        self.number_images = ["number0.png", "number1.png", "number2.png", "number3.png", "number4.png", "number5.png",
                              "number6.png", "number7.png", "number8.png", "number9.png"]
        self.image_score = [self.number_images[0]] * 4
        self.score_counter = 0

    def draw_score(self):

        for n in range(0, 4):
            score = pygame.image.load("resources/" + str(self.image_score[n] + "")).convert()
            self.parent_screen.blit(score, (self.DISPLAY_W - ((4 - n) * self.SIZE), 0))
            #self.game.draw_display()
            pygame.display.update()

    def add_score(self):
        self.score_counter += 1
        if self.units < 9:
            self.units += 1
        elif self.tens < 9:
            self.tens += 1
            self.units = 0
        elif self.hundreds < 9:
            self.hundreds += 1
            self.tens = 0
        elif self.thousands < 9:
            self.thousands += 1
            self.hundreds = 0

        self.score = [self.thousands, self.hundreds, self.tens, self.units]

        for i in range(0, 4, 1):
            self.image_score[i] = self.number_images[self.score[i]]

    def reset_score(self):
        self.thousands = 0
        self.hundreds = 0
        self.tens = 0
        self.units = 0
        self.score = [self.thousands, self.hundreds, self.tens, self.units]
        self.image_score = [self.number_images[0]] * 4
        self.score_counter = 0
