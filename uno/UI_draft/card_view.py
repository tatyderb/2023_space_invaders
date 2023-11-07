import pygame

from config import RSC, GEOM
from card import Card


class CardView:
    """ Представление класса Card."""
    bg_image = pygame.image.load(RSC['img']['card'].format('back'))

    def __init__(self, card: Card, x: int, y: int, face_up: bool = True):
        self.card = card
        self.image = pygame.image.load(RSC['img']['card'].format(repr(card)))
        self.face_up = face_up
        self.pos = (x, y)

    def draw(self, display: pygame.Surface):
        if self.face_up:
            display.blit(self.image, self.pos)
        else:
            display.blit(CardView.bg_image, self.pos)
