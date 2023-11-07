import json

from card import Card
from deck import Deck, Heap
from hand import Hand
from player import Player


class Game:
    HAND_SIZE = 7

    def __init__(self, player_names: list[str]):
        self.deck = Deck()
        self.players = [Player(name, self.deck.draw(Game.HAND_SIZE)) for name in player_names]
        self.player_index = 0
        self.heap = Heap([self.deck.draw()])

    @staticmethod
    def create(game_dict: dict):
        g = Game([])    # без игроков
        g.deck = Deck.create(game_dict['deck'])
        g.heap = Heap.create(game_dict['heap'])
        g.players = [Player(p) for p in game_dict['players']]
        g.player_index = int(game_dict['player_index'])
        return g

    @property
    def current_player(self):
        return self.players[self.player_index]

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


