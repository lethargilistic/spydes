from collections import namedtuple, UserList
from enum import Enum, unique
from random import choice, randint, sample, shuffle
from unicards import unicard

@unique
class Suit(Enum):
    JOKER = "*"
    CLUB = "C"
    SPADE = "S"
    DIAMOND = "D"
    HEART = "H"

@unique
class Value(Enum):
    ACE = 1
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
standard_values = [value for value in Value]

CardTuple = namedtuple('Card', ['Suit', 'Value'])
class Card(CardTuple):
    def __str__(self):
        string = "_A23456789TJQK"[self.Value.value]
        string += self.Suit.value
        return string
    
    def unicard(self, vary_jokers=False):
        '''Returns a unicode card representation of the card.

        If vary_jokers is True, then all three unicode jokers may be
        represented. The Value of a joker card (1,2,3) determines which is
        shown.
        
        If vary_jokers is False, then all jokers will look like the 1 joker
        card. That 1 joker is one most likely to work correctly in
        terminals, assuming not all are supported properly.'''
        if self.Suit == Suit.JOKER:
            if vary_jokers:
                return "_🃏🃟🂿"[self.Value.value]
            else:
                return "🃏"

        return unicard("_A23456789TJQK"[self.Value.value] + self.Suit.value.lower())


class Hand(UserList):
    def __init__(self, cards=[]):
        self.data = cards

    def discard_random(self, count=1):
        '''Discard [count] random cards.'''
        for _ in range(count):
            self.data.remove(choice(self.data))
    
class Deck(UserList):
    def __init__(self, cards=[]):
        self.data = cards

    def new_pack(self, packs=1, jokers=0):
        '''Fill the Deck with a new, complete set of playing card with the
        number of jokers desired'''
        self.clear() #Empty the Deck; must be first line of function

        for each_pack in range(packs):
            for number in range(jokers):
                self.data.append(Card(Suit.JOKER, Value(number%3+1)))

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

    
    def deal(self, hand, count=1):
        '''Deal from the Deck into the hand'''
        hand += self.draw(count)

    def draw(self, count=1):
        '''Draw cards from the top of the Deck. Returns a list'''
        cards = self.data[:count]
        self.data = self.data[count:]
        return cards

    def peek(self, count=1, see_all=True):
        if see_all:
            start = 0
        else:
            start = count-1

        return self.data[start:count]

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
    def shuffle_cut(self, weights):
        '''Shuffle the deck by cutting the cards'''
        new_deck = []
        for cuts in self.cut(weights):
            new_deck += cuts #self.data[cut_size*p:cut_size*(p+1)]

        self.data = new_deck

if __name__ == '__main__':
    d = Deck()
    d.new_pack(jokers=6)

    h = Hand()

    for card in h:
        print(card.unicard(True))
    print()
    for card in d:
        try:
            print(card.unicard(True))
        except ValueError:
            print(card.Value.name[0] + card.Suit.name[0].lower())
            continue
