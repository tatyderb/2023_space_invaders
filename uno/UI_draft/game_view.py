import pygame
from pygame.event import Event

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
        self.cv2 = CardView(Card('blue', 9), 200, 200)

        self.fly_card = None

    def redraw(self, display: pygame.Surface):
        # фон
        if self.background_img is None:
            display.fill(GameView.BACKGOUND_COLOR, (0, 0, self.width, self.height))
        self.cv1.draw(display)

        pygame.display.update()

    def dispatcher(self, event: Event):
        if self.fly_card:
            self.fly_card.fly()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.cv1.flip()
        if event.type == pygame.MOUSEBUTTONDOWN:
            key = pygame.mouse.get_pressed()  # key[0] - left, key[2] - right
            x, y = pygame.mouse.get_pos()
            if self.cv1.inside(x, y):
                self.cv1.flip()



