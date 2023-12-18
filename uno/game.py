import json

import pygame

from GUI.userevent import NEXT_PHASE
from card import Card
from deck import Deck, Heap
from hand import Hand
from player import Player


class Game:
    HAND_SIZE = 7
    DEFAULT_PLAYER_NAMES = ['Bob', 'Mike']

    # next_phase возвращает индекс игрока для перемещения карты:
    DECK_INDEX = -1
    HEAP_INDEX = -2

    class STATUS:
        ROUND_BEGIN = 'Round begin'
        PLAY_CARD = 'Choose card to play'
        DRAW_CARD = 'Draw card'
        PLAY_CARD_AGAIN = 'Choose card to play again'
        ROUND_END = 'Round end'
        GAME_END = 'Game over'
        ALL_STATUS = (ROUND_BEGIN, PLAY_CARD, DRAW_CARD, PLAY_CARD_AGAIN, ROUND_END, GAME_END)

    def __init__(self, player_names: list[str] | None = None):
        if player_names is None:
            player_names = Game.DEFAULT_PLAYER_NAMES
        self.deck = Deck()
        self.players = [Player(name, self.deck.draw(Game.HAND_SIZE)) for name in player_names]
        # TODO: только игрок с индексом 0 у нас интерактивный (лучше бы через конструктор)
        self.players[0].interactive = True
        self.player_index = 0
        self.heap = Heap([self.deck.draw()])
        self.__status = Game.STATUS.ROUND_BEGIN
        self.wait_interactive_action = False    # True если мы ожидаем, чтобы игрок на что-то ткнул

    @staticmethod
    def create(game_dict: dict):
        g = Game([])    # без игроков
        g.deck = Deck.create(game_dict['deck'])
        g.heap = Heap.create(game_dict['heap'])
        g.players = [Player(p) for p in game_dict['players']]
        g.player_index = int(game_dict['player_index'])
        return g

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in self.STATUS.ALL_STATUS:
            raise ValueError('Unknown game status ' + value)
        print(f'STATUS: {self.__status} -> {value}')
        self.__status = value

    @property
    def current_player(self):
        return self.players[self.player_index]

    def end_or_play(self):
        """ Есть ли карты для игры, если есть, то идет на PLAY_CARD, если нет, то END_ROUND.
        Посылает событие NEXT_PHASE.
        """
        cards = self.current_player.get_available_cards(self.heap.top())
        print(f'Available cards: {cards}')
        if cards:
            self.status = Game.STATUS.PLAY_CARD
            msg = f"{self.current_player.name} выбирает карту для игры"
        else:
            self.status = Game.STATUS.DRAW_CARD
            msg = f"{self.current_player.name} берет карту из колоды"
        pygame.event.post(pygame.event.Event(NEXT_PHASE))
        return msg

    def next_phase(self, force=False):
        """ Смена фаз машины состояний.
        return message, player_index_from, card_from, player_index_to, card_to,
        player_index_from = -1  - Deck
        player_index_to = -2    - Heap
        card_from == card_to == None - если ничего не играется
        statuses:
        ROUND_BEGIN
        PLAY_CARD
        DRAW_CARD
        PLAY_CARD_AGAIN
        ROUND_END
        """
        # Этот блок данных будем возвращать из функции
        msg = None
        player_index_from = None
        card_from = None
        player_index_to = None
        card_to = None

        print(f'\ngame.next_phase: {self.status}')

        if self.status == Game.STATUS.GAME_END:
            msg = Game.STATUS.GAME_END

        elif self.status == Game.STATUS.ROUND_END:
            self.next_player()
            self.status = Game.STATUS.ROUND_BEGIN
            msg = f"Ход переходит игроку {self.current_player.name}"
            pygame.event.post(pygame.event.Event(NEXT_PHASE))

        elif self.status == Game.STATUS.ROUND_BEGIN:
            print('\n\n\n===============================================================')
            top = self.heap.top()
            print(f'Top: {top}')
            print(self.current_player)
            msg = self.end_or_play()

        elif self.status == Game.STATUS.DRAW_CARD:
            if force:
                self.end_or_play()

            elif self.current_player.interactive:
                self.wait_interactive_action = True
                msg = f'Возьмите карту из колоды'
            else:
                msg, player_index_from, card_from, player_index_to, card_to = self.player_draw_card()

        elif self.status == Game.STATUS.PLAY_CARD or self.status == Game.STATUS.PLAY_CARD_AGAIN:
            if force:
                self.status = Game.STATUS.ROUND_END
                msg = f"Конец хода"
                pygame.event.post(pygame.event.Event(NEXT_PHASE))

            elif self.current_player.interactive:
                self.wait_interactive_action = True
                msg = f'Сыграйте карту из руки'
            else:
                msg, player_index_from, card_from, player_index_to, card_to = self.player_choose_card()

        # if not self.wait_interactive_action:
        #     pygame.event.post(pygame.event.Event(NEXT_PHASE))

        return msg, player_index_from, card_from, player_index_to, card_to

    def choose_deck(self, clicked_player_index: int):
        """ Кликнули по колоде когда игрок интерактивный и фаза DRAW_CARD"""
        return self.status == Game.STATUS.DRAW_CARD \
               and clicked_player_index == self.DECK_INDEX \
               and self.current_player.interactive

    def choose_card(self, clicked_player_index: int, card: Card):
        """ Кликнули по карте интерактивного игрока, когда его фаза игры карт и эту карту можно играть."""
        if self.status in (Game.STATUS.PLAY_CARD, Game.STATUS.PLAY_CARD_AGAIN) \
                and clicked_player_index == self.player_index and self.current_player.interactive \
                and card.accept(self.heap.top()):
            self.current_player.hand.remove_card(card)
            self.heap.put(card)
            return True
        return False

    def player_draw_card(self):
        """ Для бота и когда игрок кликнул берет карту из колоды."""
        player_index_from = self.DECK_INDEX
        card_from = self.deck.draw()
        self.current_player.hand.add_card(card_from)
        player_index_to = self.player_index
        card_to = None
        msg = f'Игрок {self.current_player.name} взял карту {card_to} из колоды'

        top = self.heap.top()
        print(f'Top: {top}')
        print(self.current_player)
        cards = self.current_player.get_available_cards(top)
        print(f'Available cards: {cards}')
        if cards:
            self.status = Game.STATUS.PLAY_CARD_AGAIN
            if self.current_player.interactive:
                self.wait_interactive_action = True

            msg = f"{self.current_player.name} выбирает карту для игры"
        else:
            self.status = Game.STATUS.ROUND_END
            msg = f"Конец раунда. Ход переходит следующему игроку."

        return msg, player_index_from, card_from, player_index_to, card_to

    def player_choose_card(self):
        """ Для бота."""
        print('>>>>>>>>>>>>>>> game.player_choose_card')
        player_index_from = self.player_index
        card_from = self.current_player.choose_card(self.heap.top())
        player_index_to = self.HEAP_INDEX
        card_to = None
        msg = f'Игрок {self.current_player.name} сыграл карту {card_from}'
        self.heap.put(card_from)

        return msg, player_index_from, card_from, player_index_to, card_to




    def run(self):
        running = True
        while running:
            top = self.heap.top()
            print(f'Top: {top}')
            print(self.current_player)
            cards = self.current_player.get_available_cards(top)
            print(f'Available cards: {cards}')
            if cards:
                # можно сыграть карту
                card = self.current_player.play_card(cards)
                self.heap.put(card)
                print(f'Play card {card}')
            else:
                # нельзя сыграть карту, берем карту из колоды
                print("Cannot play card")
                card = self.deck.draw()
                print(f'Draw card {card}')
                if top.accept(card):
                    # взятую карту можно сыграть
                    print('Play it!')
                    self.heap.put(card)
                else:
                    # взятую карту нельзя сыграть, берем ее в руку
                    self.current_player.add_card(card)
                    print('Got card :(')
            print(self.current_player)

            # проверяем условие победы, если победили, выходим с индексом игрока
            if self.current_player.check_win_condition():
                return

            self.next_player()

    def next_player(self):
        """ Переходим к следующему игроку. """
        self.player_index = (self.player_index + 1) % len(self.players)

    def congratulations(self):
        print(f'THE END! Winner {self.current_player.name}')


def new_game():
    from random import seed
    seed(7)
    g = Game(['Bob', 'Mike'])
    g.run()
    g.congratulations()

def load_game(filename: str):
    with open('data.json') as fin:
        d2 = json.load(fin)
    print(d2)
    g = Game.create(d2)
    g.run()
    g.congratulations()


if __name__ == '__main__':
    load_game('data.json')


