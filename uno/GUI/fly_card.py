import pygame

from GUI.card_view import ViewCard
from GUI.userevent import FLY_END


class FlyCard:
    """ Анимированно перемещает cv с текущей позиции на (x_to, y_to) за ticks вызвовом функции fly"""
    def __init__(self, cv: ViewCard, x_to: int, y_to: int, ticks: int):
        self.ticks = ticks
        self.cv = cv
        self.x_to = x_to
        self.y_to = y_to
        self.dx = int((x_to - self.cv.x) / ticks)
        self.dy = int((y_to - self.cv.y) / ticks)

    def fly(self):
        # print(f'fly: {self.cv}')
        self.cv.move(self.dx, self.dy)
        self.ticks -= 1
        if self.ticks <= 0:
            self.cv.set(self.x_to, self.y_to)
            pygame.event.post(pygame.event.Event(FLY_END))


