from card import Card
from hand import Hand


def test_hand():
    text = 'r4 y9 g1 b0'
    hand = Hand(Card.card_list(text))
    assert text == str(hand)

def test_acceptable_list():
    text = 'r4 y9 g1 b0'
    hand = Hand(Card.card_list(text))

    # только одна карта
    cl = hand.get_payable_cards(Card('green', 5))
    assert cl == [Card.create('g1')]

    # 2 cards
    cl = hand.get_payable_cards(Card('green', 9))
    assert cl == [Card.create('y9'), Card.create('g1')]

def test_no_playable_cards():
    text = 'r4 y9 g1'
    hand = Hand(Card.card_list(text))

    cl = hand.get_payable_cards(Card('blue', 5))
    assert cl == []

def test_remove_card():
    text = 'r4 y9 g1'
    hand = Hand(Card.card_list(text))

    hand.remove_card(Card('yellow', 9))
    assert str(hand) == 'r4 g1'

    hand.remove_card(Card('green', 1))
    assert str(hand) == 'r4'

    hand.remove_card(Card('red', 4))
    assert str(hand) == ''

def test_len():
    text = 'r4 y9 g1'
    hand = Hand(Card.card_list(text))
    assert len(hand) == 3

    text = ''
    hand = Hand(Card.card_list(text))
    assert len(hand) == 0

def test_index():
    text = 'r4 y9 g1'
    hand = Hand(Card.card_list(text))
    assert hand[0] == Card('red', 4)
    assert hand[1] == Card('yellow', 9)
    assert hand[2] == Card('green', 1)
    assert str(hand[1:]) == '[y9, g1]'



