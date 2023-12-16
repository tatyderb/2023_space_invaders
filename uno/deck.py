import random

from card import Card


class CardList:
    """ Список карт"""
    def __init__(self, cards=None):
        self.cards = [] if cards is None else cards

    def __repr__(self):
        """ r4 y9 b1 b0 """
        return ' '.join([str(c) for c in self.cards])


class Deck(CardList):
    """ Колода карт"""

    def __init__(self, cards: list[Card] | None = None):
        if cards is None:
            self.cards = Card.all_cards()
            # print(self.cards)
            random.shuffle(self.cards)
            # print(self.cards)
        else:
            super().__init__(cards)

    def draw(self, n: int = 1):
        """ Взяли из колоды 1 карту и вернули ее."""
        if n == 1:
            return self.cards.pop()
        else:
            res = self.cards[-n:]
            self.cards = self.cards[:-n]
            return res

    @staticmethod
    def create(text: str):
        return Deck(Card.card_list(text))


class Heap(CardList):

    def __str__(self):
        return repr(self.top()) if self.cards else 'Empty heap'

    def short_repr(self):
        """ __repr__ печатает все карты отбоя, тут только верхняя. """
        return repr(self.top()) if self.cards else 'Empty heap'

    def top(self) -> Card:
        """ Верхняя карта отбоя. """
        return self.cards[-1] if self.cards else None

    def put(self, card: Card):
        self.cards.append(card)

    @staticmethod
    def create(text: str):
        return Heap(Card.card_list(text))


