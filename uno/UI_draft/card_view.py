import pygame

from config import RSC, GEOM
from card import Card


class CardView:
    """ Представление класса Card."""
    bg_image = pygame.image.load(RSC['img']['card'].format('back'))
    size = (width, height) = GEOM['card']

    def __init__(self, card: Card, x: int, y: int, face_up: bool = True):
        self.card = card
        img = pygame.image.load(RSC['img']['card'].format(repr(card)))
        self.image = pygame.transform.scale(img, self.size)
        self.face_up = face_up
        self.pos = (x, y)

    def draw(self, display: pygame.Surface):
        if self.face_up:
            display.blit(self.image, self.pos)
        else:
            display.blit(CardView.bg_image, self.pos)
