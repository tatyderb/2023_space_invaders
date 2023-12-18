import pygame

from GUI.card_view import ViewCard
from GUI.config import RSC, GEOM
from GUI.fly_card import FlyCard
from GUI.player_view import VInteractivePlayer, VBotPlayer, ViewDeck, ViewHeap, VPlayer
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

        # делаем игроков, колоду и отбой; после каждого полета переделываем!
        self.vplayers: list[VBotPlayer | VInteractivePlayer] = None
        self.vdeck: ViewDeck = None
        self.vheap: ViewHeap = None
        self.need_redraw: bool = True
        self.create_table()

    def create_table(self):
        """ Часть конструктора по созданию стола"""
        print('vgame.create_table')
        rdeck, rheap, rplayer0, rplayer1 = \
            self.place_widgets(self.x, self.y + self.status_bar.rect.height,
                               self.width, self.height - self.status_bar.rect.height)
        self.vplayers: list[VPlayer] = [VInteractivePlayer(self.game.players[0], rplayer0), VBotPlayer(self.game.players[1], rplayer1)]
        self.vdeck = ViewDeck(rdeck)
        self.vheap = ViewHeap(self.game.heap.top(), rheap)
        self.need_redraw = True

    @property
    def interactive_player(self):
        return self.vplayers[0]

    def draw(self, display: pygame.Surface):
        if not self.need_redraw:
            return
        # print('vgame.redraw')
        self.need_redraw = False
        display.fill(self.BACKGROUND_COLOR, (0, 0, self.width, self.height))
        self.status_bar.draw(display)
        self.vheap.draw(display)
        self.vdeck.draw(display)
        for vp in self.vplayers:
            vp.draw(display)
        if self.fly:
            self.fly.cv.draw(display)
        pygame.display.update()

    def dispatcher(self, event: pygame.event.Event):
        """ Разбор 1 события. """
        if event.type == GAME_OVER:
            self.status_bar.text = f'Победил {self.game.current_player.name}! Нажмите q для выхода или n для новой игры.'
            self.need_redraw = True
            return

        if event.type == FLY_END:
            # надо пинуть game и сказать, что пора переходить к следующей фазе игры
            print('END OF FLY>>>>>>>>>>>')
            self.create_table()
            self.fly = None
            self.status_bar.text = 'Можно жать на кнопки'
            # если был какой-то интерактив, прекратить
            self.game.wait_interactive_action = False
            # отрабатываем следующую фазу
            self.game.next_phase(force=True)
            # pygame.event.post(pygame.event.Event(NEXT_PHASE))

        # нужна анимация - тогда ничего, кроме анимации
        if self.fly and event.type == ANIMATION:
            self.fly.fly()
            self.need_redraw = True
            return

        # переходим к новой фазе в игре
        if event.type == NEXT_PHASE:
            # не знаю откуда этот ивент, но если надо лететь, летим и не выеживаемся
            if self.fly:
                return
            msg, player_ind_from, card_from, player_ind_to, card_to = self.game.next_phase()
            self.status_bar.text = msg

            self.try_to_fly(player_ind_from, card_from, player_ind_to, card_to)
            self.need_redraw = True

        # по левому клику мыши - событие на карте
        if event.type == pygame.MOUSEBUTTONDOWN:
            key = pygame.mouse.get_pressed()    # key[0] - left, key[2] - right
            print(key)
            pos = pygame.mouse.get_pos()
            print(pos)

            # кликаем только левой кнопкой мыши
            if not key[0]:
                return

            # кликнули по нужному пользователю и карте, если ему надо выбирать карту,
            # запустили анимацию полета карты в отбой

            # если кликов не ждут, игнорируем
            if not self.game.wait_interactive_action:
                return
            # если кликнули не туда, игнорируем
            clicked_player_index, vcard, vcard_index = self.get_player_clicked_card(pos)
            card = None if vcard is None else vcard.card
            if self.game.choose_deck(clicked_player_index):
                msg, player_index_from, card_from, player_index_to, card_to = self.game.player_draw_card()
                self.status_bar.text = msg
                self.try_to_fly(player_index_from, card_from, player_index_to, card_to)
                self.need_redraw = True
            elif self.game.choose_card(clicked_player_index, card):
                print('game.choose_card')
                self.fly = FlyCard(vcard, self.vheap.bounds.x, self.vheap.bounds.y, self.TICK_ANIMATION_DURATION)
                print(f'FLY: {self.fly}')
                self.need_redraw = True


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

    def try_to_fly(self, player_index_from, card_from, player_index_to, card_to):
        """ Если нужно, начинаем полет. Только для бота! Интерактивный пользователь обрабатывает клики в другом месте"""
        print(f'vgame.try_to_fly({player_index_from=}, {card_from=}, {player_index_to=}, {card_to=})')
        if card_from is None and card_to is None:
            return
        if player_index_from == self.game.DECK_INDEX:
            vp = self.vplayers[player_index_to]
            deck_bounds = self.vdeck.bounds
            vc = ViewCard(card_from, deck_bounds.x, deck_bounds.y, face_up=self.game.current_player.interactive)
            self.fly = FlyCard(vc, vp.empty.x, vp.empty.y, self.TICK_ANIMATION_DURATION)
        if player_index_to == self.game.HEAP_INDEX:
            for cv in self.vplayers[player_index_from].hand:
                if cv.card == card_from:
                    print(f'{cv.card=} vs {card_from=}')
                    cv.face_up = True
                    self.fly = FlyCard(cv, self.vheap.bounds.x, self.vheap.bounds.y, self.TICK_ANIMATION_DURATION)
                    break

    @classmethod
    def create(cls, filename):
        pass

    def place_widgets(self, x, y, width, height) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]:
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

    def get_player_clicked_card(self, pos) -> tuple[int, ViewCard, int]:
        """ По позиции мыши pos возвращает по какому игроку и какой его карте был клик clicked_player_index, vcard"""
        clicked_player_index = None
        vcard = None
        vcard_index = None
        if self.vdeck.bounds.collidepoint(pos):
            print('vgame.get_player_clicked_card: DECK')
            clicked_player_index = self.game.DECK_INDEX
            vcard = None
        elif self.vheap.bounds.collidepoint(pos):
            print('vgame.get_player_clicked_card: HEAP')
            clicked_player_index = self.game.HEAP_INDEX
            vcard = None
        else:
            for i, vplayer in enumerate(self.vplayers):
                if vplayer.bounds.collidepoint(pos):
                    print(f'vgame.get_player_clicked_card: PLAYER {i}')
                    clicked_player_index = i
                    vcard, vcard_index = self.vplayers[i].get_vcard(pos)
                    print(f'vgame.get_player_clicked_card: PLAYER {i} {vcard=} {vcard_index=}')

        return clicked_player_index, vcard, vcard_index
