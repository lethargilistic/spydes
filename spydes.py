from collections import namedtuple, UserList
from enum import Enum, unique
from random import randint, sample, shuffle

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

CardTuple = namedtuple('Card', ['Suit', 'Value'])
class Card(CardTuple):
    def __str__(self):
        return "" + str(self.Suit) + "|" + str(self.Value)
    
class Deck(UserList):
    def __init__(self, cards=[]):
        self.data = cards

    def new_pack(self, jokers=0):
        '''Fill the Deck with a new, complete set of playing card with the
        number of jokers desired'''
        self.clear()

        for _ in range(jokers):
            self.data.append(Card(Suit.JOKER, Value.JOKER))

        for suit in standard_suits:
            for value in standard_values:
                self.data.append(Card(suit, value))

    def found_pack(self):
        '''I found this abandoned pack of playing cards at the library. It's
        probably not complete... But what if it is...? Oh, wow. Who cares? Look
        at the design on the back! I'm keeping these.'''
        self.clear() #Empty the Deck; must be first line of function
        
        full_deck = Deck()
        full_deck.new_pack(jokers=randint(0,2))

        self.data = sample(full_deck, randint(0,len(full_deck)))

    def draw(self):
        '''Draw a card from the top of the Deck. Alias for list.pop().'''
        return self.pop()

    def shuffle(self):
        '''Shuffle the Deck.'''
        shuffle(self.data)

    def cut(self, weights):
        '''Cut the deck, return the cuts as list elements. Each slice is given an
        integer weight, in order, from the list `weights`.  The slices are
        returned in the order of their weight. This means that a simple [1,0,2]
        will work, as will [2,1,3], as will [0, -765, 100000].'''
        #https://stackoverflow.com/a/7851166
        positions = sorted(range(len(weights)), key=lambda k: weights[k])

        cut_size = len(self.data) // len(weights)

        deck_cuts = []
        for p in positions:
            deck_cuts.append(self.data[cut_size*p:cut_size*(p+1)])

        return deck_cuts

    #FIXME: Doesn't detect if there are more weights than cards.
    #FIXME: Might have a bug where it loses a card if the slices are not even.
    #For example, four cards and three slices. Testing needed.
    def cut_shuffle(self, weights):
        new_deck = []
        for cuts in self.cut(weights):
            new_deck += cuts #self.data[cut_size*p:cut_size*(p+1)]

        self.data = new_deck

if __name__ == '__main__':
    d = Deck()
    d.new_pack()
    d.shuffle()

    for card in d:
        print(card)
