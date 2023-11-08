""" Отрисовка анимации полета карты."""
import pygame

from UI_draft.userevent import FLY_END_EVENT
from card import Card
from UI_draft.card_view import CardView


class FlyAnimation:

    def __init__(self, cv: CardView, x_to: int, y_to: int, ticks = 60):
        self.cv = cv
        self.x_to = x_to
        self.y_to = y_to
        self.ticks = ticks
        self.dx = int((x_to - cv.x) / ticks)
        self.dy = int((y_to - cv.y) / ticks)

    def fly(self):
        self.ticks -= 1
        self.cv.move(self.dx, self.dy)
        if self.ticks <= 0:
            pygame.event.post(FLY_END_EVENT)
            self.cv.set_pos(self.x_to, self.y_to)

    def draw(self, display: pygame.Surface):
        self.cv.draw(display)
