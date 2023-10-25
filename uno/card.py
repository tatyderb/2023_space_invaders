import pytest

class Card:
    COLORS = ['red', 'green', 'blue', 'yellow']
    NUMBERS = list(range(10)) + list(range(1, 10))
    COLOR_LETTERS = {'r': 'red', 'g': 'green', 'b': 'blue', 'y': 'yellow'}


    def __init__(self, color, number):
        if color in self.COLORS:
            self.color = color  # 'red' vs 'r'
        else:
            raise ValueError(f'Wrong color {color}')

        if 0 <= number <= 9:
            self.number = number
        else:
            raise ValueError(f'Wrong number {number}')

    def __repr__(self):
        return f'{self.color[0]}{self.number}'

    def __eq__(self, other):
        return self.color == other.color and self.number == other.number

    @staticmethod
    def create(text: str):
        """ По тексту вида 'r4' возвращается карта Card('red', 4)."""
        letter = Card.COLOR_LETTERS.get(text[0], None)
        number = int(text[1:])
        return Card(letter, number)

    @staticmethod
    def card_list(text: str):
        """ Из строки вида 'y9 r9 y0 y1' возвращает список соответствующих карт."""
        return [Card.create(word) for word in text.split()]

    @staticmethod
    def all_cards():
        """ Все карты для создания колоды. """
        return [Card(color, number) for number in Card.NUMBERS for color in Card.COLORS]


