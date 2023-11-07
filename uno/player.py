""" Игрок """
from card import Card
from hand import Hand


class Player:
    def __init__(self, name: str, hand: Hand | None = None):
        self.name = name
        self.hand = Hand([] if hand is None else hand)

    def __repr__(self):
        return f'{self.name}: {self.hand}'

    def add_card(self, card: Card):
        self.hand.add_card(card)

    def check_win_condition(self) -> bool:
        return len(self.hand) == 0

    def play_card(self, cards: list[Card]) -> Card:
        """ играет карту, удаляя ее из руки. Возвращает сыгранную карту. """
        card = cards[0]
        print(self.hand, type(self.hand))
        self.hand.remove_card(card)
        return card

    @staticmethod
    def create(player_dict: dict):
        """ {'name': 'Bob', 'hand': 'r4 b7 y2'} """
        return Player(player_dict['name'], Hand.create(player_dict['hand']))

    def get_available_cards(self, top: Card):
        """ Возвращает список карт, которые можно положить на top"""
        return [card for card in self.hand if top.accept(card)]

