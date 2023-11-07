import pygame

from config import RSC, GEOM
from card import Card


class CardView:
    """ Представление класса Card."""
    size = (width, height) = GEOM['card']
    bg_image = pygame.transform.scale(pygame.image.load(RSC['img']['card'].format('back')), size)

    def __init__(self, card: Card, x: int, y: int, face_up: bool = True):
        self.card = card
        img = pygame.image.load(RSC['img']['card'].format(repr(card)))
        self.image = pygame.transform.scale(img, self.size)
        self.face_up = face_up
        self.x = x
        self.y = y

    def draw(self, display: pygame.Surface):
        if self.face_up:
            display.blit(self.image, (self.x, self.y))
        else:
            display.blit(CardView.bg_image, (self.x, self.y))

    def inside(self, x, y):
        r = pygame.Rect(self.x, self.y, self.width, self.height)
        return r.collidepoint(x, y)

    def flip(self):
        """ Переворачивает карту. """
        self.face_up = not self.face_up
