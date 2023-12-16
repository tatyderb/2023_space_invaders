import pygame

from GUI.card_view import ViewCard
from GUI.config import RSC, GEOM
from GUI.fly_card import FlyCard
from GUI.player_view import VInteractivePlayer, VBotPlayer, ViewDeck, ViewHeap
from GUI.status_bar import StatusBar
from GUI.userevent import *
from card import Card
from game import Game


class ViewGame:
    BACKGROUND_COLOR = RSC['img']['bg_color']
    TICK_MS = int(1000 / RSC['FPS'])                # милисекунд между тиками анимации
    TICK_ANIMATION_DURATION = int(1000 / TICK_MS)   # за сколько тиков отработает анимация

    def __init__(self, size, game: Game):
        # Одна карта, клик мыши левой кнопкой - переворот карты, a - select/unselect
        pygame.time.set_timer(ANIMATION, self.TICK_MS)
        self.size = self.width, self.height = size
        self.x, self.y = 0, 0
        self.status_bar = StatusBar(pygame.Rect(0, 0, self.width, 0))
        self.fly: FlyCard | None = None
        self.game = game
        # прибьем гвоздями игроков: человека и пока 1 бота
        if len(game.players) != 2:
            raise ValueError('Пока играем в 2 игрока')
        rdeck, rheap, rplayer0, rplayer1 = \
            self.place_widgets(self.x, self.y + self.status_bar.rect.height,
                               self.width, self.height - self.status_bar.rect.height)
        self.vplayers = [VInteractivePlayer(game.players[0], rplayer0), VBotPlayer(game.players[1], rplayer1)]
        self.vdeck = ViewDeck(rdeck)
        self.vheap = ViewHeap(game.heap.top(), rheap)
        # self.cv1 = ViewCard(Card('red', 4), 10, 50)
        # self.cv2 = ViewCard(Card('yellow', 9), 400, 250)

    def draw(self, display: pygame.Surface):
        display.fill(self.BACKGROUND_COLOR, (0, 0, self.width, self.height))
        # self.cv1.draw(display)
        # self.cv2.draw(display)
        self.status_bar.draw(display)
        self.vheap.draw(display)
        self.vdeck.draw(display)
        for vp in self.vplayers:
            vp.draw(display)
        pygame.display.update()

    def dispatcher(self, event: pygame.event.Event):
        """ Разбор 1 события. """
        if event.type == FLY_END:
            # надо пинуть game и сказать, что пора переходить к следующей фазе игры
            print('END OF FLY>>>>>>>>>>>')
            self.fly = None
            self.status_bar.text = 'Можно жать на кнопки'

        # нужна анимация - тогда ничего, кроме анимации
        if self.fly and event.type == ANIMATION:
            self.fly.fly()
            return

        # по левому клику мыши - событие на карте
        if event.type == pygame.MOUSEBUTTONDOWN:
            key = pygame.mouse.get_pressed()    # key[0] - left, key[2] - right
            print(key)
            pos = pygame.mouse.get_pos()
            print(pos)
            # нажата левая кнопка мыши, смотрим попало событие в widget
        #     if key[0] and self.cv1.inside(pos):
        #         self.cv1.flip()
        #         self.status_bar.text = 'Перевернули карту'
        #     # для второй карты нажатие запускает полет
        #     if key[0] and self.cv2.inside(pos):
        #         self.fly = FlyCard(self.cv2, self.cv1.x, self.cv1.y, self.TICK_ANIMATION_DURATION)
        #         self.status_bar.text = 'Полетели!'
        #
        # # по клавише a - select/unselect
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #     self.cv1.select()

    def model_update(self):
        pass

    @classmethod
    def create(cls, filename):
        pass

    def place_widgets(self, x, y, width, height) -> tuple[pygame.Rect]:
        """ Размещаем игроков и руки, возвращает rdeck, rheap, rplayer0, rplayer1"""
        # пока расчет на 2 игроков
        h = height // 3
        rplayer0 = pygame.Rect(x, y, width, h)
        rplayer1 = pygame.Rect(x, y + 2 * h, width, h)
        w = width // 4
        wcard, hcard = GEOM['card']
        ydeck = int(y + 1.5 * h - hcard // 2)
        rheap = pygame.Rect(x + w - wcard // 2, ydeck, wcard, hcard)
        rdeck = pygame.Rect(int(x + 3 * w - wcard // 2), ydeck, wcard, hcard)
        return rdeck, rheap, rplayer0, rplayer1


