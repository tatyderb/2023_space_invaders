import pygame

from GUI.config import RSC, GEOM
from card import Card


class ViewCard:
    BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(RSC['img']['back']), GEOM['card'])

    def __init__(self, card: Card, x: int, y: int, face_up: bool = True):
        self.card = card
        filename = RSC['img']['card'].format(repr(card))
        # print(filename)
        img = pygame.image.load(filename)
        self.img = pygame.transform.scale(img, GEOM['card'])
        self.x = x
        self.y = y
        self.width, self.height = GEOM['card']
        self.face_up = face_up

    def draw(self, display: pygame.Surface):
        if self.face_up:
            display.blit(self.img, (self.x, self.y))
        else:
            display.blit(self.BACKGROUND_IMG, (self.x, self.y))

    def flip(self):
        """ Переворачивает карту. """
        self.face_up = not self.face_up

    def inside(self, pos: tuple[int, int]):
        """ pos внутри этой карты"""
        r = pygame.Rect(self.x, self.y, self.width, self.height)
        return r.collidepoint(pos)



