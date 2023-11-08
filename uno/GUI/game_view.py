import pygame

from GUI.card_view import ViewCard
from GUI.config import RSC
from card import Card


class ViewGame:
    BACKGROUND_COLOR = RSC['img']['bg_color']
    def __init__(self, size):
        # Одна карта, клик мыши левой кнопкой - переворот карты, a - select/unselect
        self.cv = ViewCard(Card('red', 4), 10, 20)
        self.size = self.width, self.height = size

    def draw(self, display: pygame.Surface):
        display.fill(self.BACKGROUND_COLOR, (0, 0, self.width, self.height))
        self.cv.draw(display)
        pygame.display.update()

    def dispatcher(self, event: pygame.event.Event):
        """ Разбор 1 события. """
        # по левому клику мыши - событие на карте
        if event.type == pygame.MOUSEBUTTONDOWN:
            key = pygame.mouse.get_pressed()    # key[0] - left, key[2] - right
            print(key)
            pos = pygame.mouse.get_pos()
            print(pos)
            # нажата левая кнопка мыши, смотрим попало событие в widget
            if key[0] and self.cv.inside(pos):
                self.cv.flip()

