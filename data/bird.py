import pygame


class Bird:
    R = 13

    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.gravity = 0.5
        self.velocity = 0
        self.lift = -12

    def update(self):
        self.velocity += self.gravity
        if self.velocity >= 5:
            self.velocity = 5
        self.y += self.velocity

        height = self.screen.get_height()
        if self.y >= height:
            self.y = height
            self.velocity = 0
        if self.y <= 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        self.velocity += self.lift

    def hits(self, pipe):
        if self.y - self.R < pipe.top or self.y + self.R > pipe.bottom:
            if self.x + self.R > pipe.x and self.x - self.R < pipe.x + pipe.W:
                return True
        return False

    def show(self):
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (round(self.x), round(self.y)), Bird.R)

    def passed(self, pipe):
        if self.x > pipe.x:
            return True
        else:
            return False

    def fall(self):
        height = self.screen.get_height()
        if self.y >= height:
            return True
        return False
