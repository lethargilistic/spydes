from enum import Enum, unique
from collections import namedtuple, UserList

@unique
class Suit(Enum):
    JOKER = 0
    CLUB = 1
    SPADE = 2
    DIAMOND = 3
    HEART = 4

@unique
class Value(Enum):
    JOKER = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

standard_suits = [suit for suit in Suit if suit != Suit.JOKER]
standard_values = [value for value in Value if value != Value.JOKER]
Card = namedtuple('Card', ['Suit', 'Value'])
    
class Deck(UserList):
    def __init__(self, cards=[]):
        self._deck_holder = self.data = cards

    def fill(self, jokers=0):
        for _ in range(jokers):
            self._deck_holder.append(Card(Suit.JOKER, 0))

        for suit in standard_suits:
            for value in standard_values:
                self._deck_holder.append(Card(suit, value))

    def draw(self):
        return self.pop()

    def insert(card, position=0):
        self.insert(card)

if __name__ == '__main__':
    d = Deck()
    d.fill(jokers=2)

    for card in d:
        print(card)
