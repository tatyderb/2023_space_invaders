from card import Card
from deck import CardList


class Hand(CardList):
    """ Рука игрока"""

    def __len__(self):
        """ Возвращает размер руки."""
        return len(self.cards)

    def __getitem__(self, item):
        """дает hand[i] и hand[i:j]"""
        return self.cards[item]

    def get_payable_cards(self, topcard: Card):
        """ Возвращает список карт, которые можно было бы сыграть на topcard"""
        return [card for card in self.cards if topcard.accept(card)]

    def remove_card(self, card: Card):
        """ Удаляет из руки карту card (чтобы положить ее в отбой)"""
        self.cards.remove(card)
        # self.cards = [c for c in self.cards if c != card]

    def add_card(self, card: Card):
        """ Добавляет карту в руку. """
        self.cards.append(card)

    @staticmethod
    def create(text: str):
        return Hand(Card.card_list(text))

