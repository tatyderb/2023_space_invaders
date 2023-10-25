import pytest

from card import Card


def test_card():
    c = Card('blue', 9)
    assert c.color == 'blue'
    assert c.number == 9

def test_create():
    c = Card.create('r4')
    # assert c == Card('red', 4)
    assert c == Card('red', 4)
    assert str(c) == 'r4'

def test_create_wrong_color():
    with pytest.raises(ValueError):
        c = Card.create('a4')

def test_create_wrong_number():
    with pytest.raises(ValueError):
        c = Card.create('r14')

def test_create_card_list():
    text = "y9 r9 y0 y1"
    assert Card.card_list(text) == [Card("yellow", 9), Card('red', 9), Card('yellow', 0), Card('yellow', 1)]

def test_accept():
    tc = Card('blue', 9)
    c = Card('blue', 1)
    assert tc.accept(c)
    assert c.accept(tc)
    assert tc.accept(Card('green', 9))
    assert tc.accept(Card('blue', 9))

    assert not tc.accept(Card('green', 8))
    assert not tc.accept(Card('red', 4))

