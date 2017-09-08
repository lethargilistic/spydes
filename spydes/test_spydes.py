import pytest

from spydes import *

def test_Deck():
    d = Deck()
    d.new_pack()

    assert len(d) == 52

def test_Deck_rotate__once():
    d = Deck([Card(Suit.heart, Value.ace), Card(Suit.club, Value.ace), Card(Suit.spade, Value.ace)])
    d.rotate()
    assert d == [Card(Suit.club, Value.ace), Card(Suit.spade, Value.ace), Card(Suit.heart, Value.ace)]

def test_Card_same_value__one_joker_equal_value():
    '''fails because a joker is only equal to another joker.'''
    first_card = Card(Suit.club, Value.three)
    second_card = Card(Suit.joker, Value.three)
    assert not first_card.same_value(second_card)

def test_Card_same_suit__equal_suits():
    first_card = Card(Suit.heart, Value.two)
    second_card = Card(Suit.heart, Value.three)
    assert first_card.same_suit(second_card)

def test_Card_same_suit__unequal_suits():
    first_card = Card(Suit.club, Value.two)
    second_card = Card(Suit.heart, Value.three)
    assert not first_card.same_suit(second_card)

def test_Card_same_suit__jokers_unequal_value():
    first_card = Card(Suit.joker, Value.three)
    second_card = Card(Suit.joker, Value.two)
    assert first_card.same_suit(second_card)

def test_Deck_unicards__vary_jokers():
    d = Deck()
    d.new_pack(jokers=5)
    correct = '🃟 🂿 🃏 🃟 🂿 🂡 🂢 🂣 🂤 🂥 🂦 🂧 🂨 🂩 🂪 🂫 🂭 🂮 🂱 🂲 🂳 🂴 🂵 🂶 🂷 🂸 🂹 🂺 🂻 🂽 🂾 🃁 🃂 🃃 🃄 🃅 🃆 🃇 🃈 🃉 🃊 🃋 🃍 🃎 🃑 🃒 🃓 🃔 🃕 🃖 🃗 🃘 🃙 🃚 🃛 🃝 🃞 '
    assert d.unicard(vary_jokers=True) == correct
