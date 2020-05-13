import pygame
import random


class Pipe:
    W = 40

    def __init__(self, screen):
        self.screen = screen
        gap = random.randint(100, 200)
        self.top = random.randint(0, (screen.get_height() - gap))
        self.bottom = gap + self.top
        self.x = screen.get_width()
        self.speed = 2

    def update(self):
        self.x -= self.speed

    def show(self, ishit):
        color = (255, 255, 255)

        if ishit:
            color = (255, 0, 100)

        pygame.draw.rect(self.screen, color,
                         (self.x, 0, self.W, self.top))
        pygame.draw.rect(self.screen, color,
                         (self.x, self.bottom, self.W, self.screen.get_height() - self.bottom))

    def offscreen(self):
        if self.x < -self.W:
            return True
        return False
