import pygame
import random


class Apple:

    def __init__(self, parent_screen, size):
        self.SIZE = size
        self.appleImage = pygame.image.load("resources/apple.png").convert_alpha()
        self.parent_screen = parent_screen
        self.x = round(random.uniform(0, 1) * 19) * self.SIZE
        self.y = round(random.uniform(0, 1) * 19) * self.SIZE
        self.clear_block = pygame.image.load("resources/level1_bg.png")

    def draw(self):
        self.parent_screen.blit(self.appleImage, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = round(random.uniform(0, 1) * 19) * self.SIZE
        self.y = round(random.uniform(0, 1) * 19) * self.SIZE

    def clear(self):
        self.parent_screen.blit(self.clear_block, (self.x, self.y), (self.x, self.y, 50, 50))
