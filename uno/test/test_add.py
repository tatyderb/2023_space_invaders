from add import add, sub
import pytest

def test_add_int():
    assert 5 == add(2, 3)
    assert add(2, 4) == 6
    assert add(3, 3) == 6
    assert add(2, -5) == -3, 'С отрицательным'


def test_add_float():
    assert 5.3 == add(2.3, 3.)
    assert add(2, 4) == 6
    assert add(3, 3) == 6
    assert add(2, -5) == -3, 'С отрицательным'
