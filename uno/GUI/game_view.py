import pygame

from GUI.card_view import ViewCard
from GUI.config import RSC
from card import Card


class ViewGame:
    BACKGROUND_COLOR = RSC['img']['bg_color']
    def __init__(self, size):
        # Одна карта, клик мыши левой кнопкой - переворот карты, a - select/unselect
        self.cv1 = ViewCard(Card('red', 4), 10, 20)
        self.cv2 = ViewCard(Card('yellow', 9), 400, 250)
        self.size = self.width, self.height = size
        self.fly: FlyCard = None

    def draw(self, display: pygame.Surface):
        display.fill(self.BACKGROUND_COLOR, (0, 0, self.width, self.height))
        self.cv1.draw(display)
        self.cv2.draw(display)
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
            if key[0] and self.cv1.inside(pos):
                self.cv1.flip()

        # по клавише a - select/unselect
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self.cv1.select()

