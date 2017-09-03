import pytest

from spydes import *

def test_Deck():
    d = Deck()
    d.new_pack()

    assert len(d) == 52

def test_Deck_rotate_once():
    d = Deck([Card(Suit.heart, Value.ace), Card(Suit.club, Value.ace), Card(Suit.spade, Value.ace)])
    d.rotate()
    assert d == [Card(Suit.club, Value.ace), Card(Suit.spade, Value.ace), Card(Suit.heart, Value.ace)]
