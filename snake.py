

import pygame
from game import *
import apple


class Snake:

    def __init__(self, parent_screen, length, position, size, rotation):
        self.position = position
        self.SIZE = size
        self.length = length
        self.rotation = [rotation] * self.length  # addition
        self.parent_screen = parent_screen
        self.clear_block = pygame.image.load("resources/level1_bg.png")
        self.body_part = ["head", "body1", "tail", "bend1", "headeat", "bodyeat", "headeaten","bendtail","bendtail1"]
        self.eat = "none"
        self.swallow = "none"
        self.block = []
        self.clear_buff_x = 0  # del
        self.clear_buff_y = 0   # del

        self.x = [(3 - x) * self.position for x in range(self.length)]
        self.y = [self.position] * self.length

        # self.y = [self.position] * self.length
        # self.x = [self.position] * self.length

        # for i in range(0, self.length, 1):
        #     self.x[i] = ((3-i) * self.position)

        for i in range(0, len(self.body_part), 1):
            self.block.append(pygame.image.load(f"resources/{self.body_part[i]}.png").convert_alpha())

        self.direction = "start"
        self.live = True
        self.speed = 0.30

    def clear(self):
        if self.direction != "start":
            # self.parent_screen.blit(self.clear_block, (self.x[-1], self.y[-1]), (self.x[-1], self.y[-1], 50, 50))
            self.parent_screen.blit(self.clear_block, (self.clear_buff_x, self.clear_buff_y),
                                    (self.clear_buff_x, self.clear_buff_y, 50, 50)) # del
        # this clears th block left behind by the snake walking by drawing the section on the background that would have
        # been there...
        # display.blit(bg,(loc to plc bg in display(x,y)),(loc to draw bg from (x,y),pixels dwn & rht from loc (x,y))
        # flip shows the snake, like flipping a clip board to show the audience.


    def set_bend(self, i):

        self.rotation[i] = self.rotation[i] - 180

        if 270 > abs(self.rotation[i] - self.rotation[i-1]) >= 90:

            if self.rotation[i-1] < self.rotation[i]:

                self.rotation[i] = self.rotation[i-1]

        elif abs(self.rotation[i] - self.rotation[i - 1]) == 270:

            if self.rotation[i - 1] > self.rotation[i]:

                self.rotation[i] = self.rotation[i - 1]

    def draw_head(self, parent_screen, block, rotation):
        # new stuff - draw head
        body_part = 0

        if self.eat == 1:
            body_part = 6
            self.eat = "none"
            self.swallow = 1

        if self.eat == 0:
            body_part = 4
            self.eat = 1

        rotated_image = pygame.transform.rotate(block[body_part], rotation[0])
        new_rect = rotated_image.get_rect(center=block[body_part].get_rect(topleft=(self.x[0], self.y[0])).center)
        parent_screen.blit(rotated_image, new_rect)

    def check_swallow(self):

        if isinstance(self.swallow, int):

            if self.swallow < self.length-1:

                self.swallow += 1
            elif self.swallow >= self.length-1:
                self.swallow = "none"

    def draw_body(self, parent_screen, block, rotation):
        for i in range(1, self.length, 1):  # for loop old keep

            rotation_buffer = self.rotation[i]  # saves the rotation of body part 'i' as it is changed in bend()
        # -------------setting straight (default) body parts------------------------


            if i < self.length-1:

                body_part = 1  # setting body_part to straight mid body ( default mid body)

            else:

                body_part = 2  # setting body_part to straight tail ( default tail)

            if isinstance(self.swallow, int):

                if 1 <= self.swallow < self.length-1:  #-2

                    if self.swallow == i:

                        if abs((rotation[i] - rotation[i - 1])) == 0:

                            body_part = 5
                        else:
                            self.swallow += 1
        # ----------------------------Setting 'tail bend' body part---------------------------------------------
            if abs((rotation[i] - rotation[i - 1])) >= 90:

                if i != self.length - 1:

                    body_part = 3  # setting body_part to mid body bend,(block(3))

                else:

                    if rotation[i] < rotation[i - 1]:

                        body_part = 7

                        if rotation[i - 1] == 270 and rotation[i] == 0:

                            body_part = 8  # setting body_part to tail bend (block(8))

                    if rotation[i] > rotation[i-1]:

                        body_part = 8

                        if rotation[i - 1] == 0 and rotation[i] == 270:

                            body_part = 7  # setting body_part to tail bend (block(7))

                self.set_bend(i)

            # draws tail or mid mid body (bended, bulging or not straight)
            rotated_image = pygame.transform.rotate(block[body_part], rotation[i])
            new_rect = rotated_image.get_rect(center=block[body_part].get_rect(topleft=(self.x[i], self.y[i])).center)
            # update the coordinates of each block in the snake and show this on the screen
            parent_screen.blit(rotated_image, new_rect)

            self.rotation[i] = rotation_buffer

        self.check_swallow()



    def draw(self, parent_screen, block, rotation):

        # draw snake head
        # if self.eat != 0:
        self.draw_head(parent_screen, block, rotation)

        # draw snake body

        self.draw_body(parent_screen, block, rotation)

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def keep_still(self):
        self.direction = "none"

    def walk(self):

        if self.direction != "start":

            # use a touple instead to save x and y pos into 1 variable
            self.clear_buff_x = self.x[self.length-1]  # used to save the x -pos of the tail before snake walks
            self.clear_buff_y = self.y[self.length-1]  # used to save the y -pos of the tail before snake walks

            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]
                self.rotation[i] = self.rotation[i - 1]

            if self.direction == "right":
                self.rotation[0] = 0
                if 1000 <= self.x[0] <= 1000 + self.SIZE:
                    self.x[0] = 0
                else:
                    self.x[0] += self.SIZE

            if self.direction == "left":
                self.rotation[0] = 180
                if 0 >= self.x[0] >= 0 - self.SIZE:
                    self.x[0] = 1000
                else:
                    self.x[0] -= self.SIZE

            if self.direction == "up":
                self.rotation[0] = 90
                if 0 >= self.y[0] >= 0 - self.SIZE:
                    self.y[0] = 1000
                else:
                    self.y[0] -= self.SIZE

            if self.direction == "down":
                self.rotation[0] = 270
                if 1000 <= self.y[0] <= 1000 + self.SIZE:
                    self.y[0] = 0
                else:
                    self.y[0] += self.SIZE

        self.draw(self.parent_screen, self.block, self.rotation)

        if self.direction != "start":
            self.clear()


    def increase_length(self):
        # append(-1)
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        self.rotation.append(-1)
        self.rotation[-1] = self.rotation[-2]

    def reset_snake(self):

        self.length = 3

        self.x = [(3 - x) * self.position for x in range(self.length)]  # use of list comprehension to initialise list
        self.y = [self.position] * self.length
        self.rotation = [0] * self.length
        self.direction = "start"
        self.live = True
        self.speed = 0.30
