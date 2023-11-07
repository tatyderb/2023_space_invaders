import pygame

from UI_draft.card_view import CardView
from UI_draft.config import RSC
from card import Card


class GameView:
    BACKGOUND_COLOR = (0, 81, 44)

    def __init__(self, width: int, height: int, filename: str = None):
        """ Создает новую или загружает игру из filename. """
        # TODO: подключаем всю игру
        # self.game = Game()

        # геометрия
        self.width = width
        self.height = height

        # поле игры
        # TODO: подобрать красивое изображение
        # self.background_img = pygame.image.load(RSC['img']['background'])
        self.background_img = None

        # тест одной карты, переворачиваем рубашку по клику мыши
        self.cv1 = CardView(Card('red', 4), 20, 10)

    def redraw(self, display: pygame.Surface):
        # фон
        if self.background_img is None:
            display.fill(GameView.BACKGOUND_COLOR, (0, 0, self.width, self.height))
        self.cv1.draw(display)

        pygame.display.update()
