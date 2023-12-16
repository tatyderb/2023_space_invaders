import pygame

from GUI.config import RSC, GEOM
from card import Card


class ViewCard:
    BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(RSC['img']['back']), GEOM['card'])
    SELECTED_GAP_X = 4
    SELECTED_GAP_Y = 6
    SELECTED_COLOR = 'magenta'

    def __init__(self, card: Card | None, x: int, y: int, face_up: bool = True):
        """ card = None - пустое место под карту. """
        self.card = card
        self.x = x
        self.y = y
        self.width, self.height = GEOM['card']
        self.face_up = face_up
        self.selected = False

    @property
    def card(self):
        return self.__card

    @card.setter
    def card(self, value: Card):
        self.__card = value
        if value is not None:
            filename = RSC['img']['card'].format(repr(value))
            # print(filename)
            img = pygame.image.load(filename)
            self.img = pygame.transform.scale(img, GEOM['card'])
        else:
            self.img = None

    def draw(self, display: pygame.Surface):
        # отрисовка рамки, если selected
        if self.card is None:
            return
        if self.selected:
            x = self.x - self.SELECTED_GAP_X
            y = self.y - self.SELECTED_GAP_Y
            w = self.width + 2 * self.SELECTED_GAP_X
            h = self.height + 2 * self.SELECTED_GAP_Y
            display.fill(self.SELECTED_COLOR, (x, y, w, h))
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

    def select(self, selected: bool | None = None):
        """ Устанавливает выделение на карте, или меняет его если selected is None """
        if selected is None:
            self.selected = not self.selected
        else:
            self.selected = selected

    def move(self, dx: int, dy: int):
        """ Сдвигает карту на dx, dy """
        self.x += dx
        self.y += dy

    def set(self, x_to, y_to):
        self.x = x_to
        self.y = y_to



