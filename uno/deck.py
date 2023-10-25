import random

from card import Card


class Deck:
    """ Колода карт"""

    def __init__(self, cards: list[Card] | None = None):
        if cards is None:
            self.cards = Card.all_cards()
            # print(self.cards)
            random.shuffle(self.cards)
            # print(self.cards)
        else:
            self.cards = cards

    def __repr__(self):
        """ r4 y9 b1 b0 """
        return ' '.join([str(c) for c in self.cards])

    def draw(self):
        """ Взяли из колоды 1 карту и вернули ее."""
        card = self.cards.pop()
        return card
