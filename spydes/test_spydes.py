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

def test_Card_same_value():
    first_card = Card(Suit.club, Value.three)
    second_card = Card(Suit.joker, Value.three)
    assert first_card.same_value(second_card)

def test_Deck_unicards_varyjokers():
    d = Deck()
    d.new_pack(jokers=5)
    correct = '🃟 🂿 🃏 🃟 🂿 🂡 🂢 🂣 🂤 🂥 🂦 🂧 🂨 🂩 🂪 🂫 🂭 🂮 🂱 🂲 🂳 🂴 🂵 🂶 🂷 🂸 🂹 🂺 🂻 🂽 🂾 🃁 🃂 🃃 🃄 🃅 🃆 🃇 🃈 🃉 🃊 🃋 🃍 🃎 🃑 🃒 🃓 🃔 🃕 🃖 🃗 🃘 🃙 🃚 🃛 🃝 🃞 '
    assert d.unicard(vary_jokers=True) == correct
