from collections import namedtuple, UserList
from enum import Enum, unique
from math import ceil, floor
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
                return "_🃏🃟🂿"[self.Value.value%3+1] #%3+1 is just extra assurance
            else:
                return "🃏"

        return unicard("_A23456789TJQK"[self.Value.value] + self.Suit.value.lower())

class Deck(UserList):
    def __init__(self, cards=[]):
        self.data = cards
    
    def __str__(self):
        string = '[' + str(self.data[0])
        for card in self.data[1:]:
            string += ', ' + str(card)
        return string + ']'

    def new_pack(self, packs=1, jokers=0):
        '''Fill the Deck with a new, complete set of playing card with the
        number of jokers desired'''
        self.clear() #Empty the Deck; must be first line of function

        for each_pack in range(packs):
            for number in range(jokers):
                #%3+1 puts Joker within the range of the three Unicode jokers
                self.data.append(Card(Suit.JOKER, Value(number%3+1)))

            for suit in standard_suits:
                for value in standard_values:
                    self.data.append(Card(suit, value))

    def fill_suit(self, suit):
        '''Add all cards of suit'''
        pass

    def fill_value(self, value):
        '''Add all cards of value, excluding Jokers'''
        pass

    def found_pack(self):
        '''I found this abandoned pack of playing cards at the library. It's
        probably not complete... But what if it is...? Oh, wow. Who cares? Look
        at the design on the back! I'm keeping these.'''
        self.clear() #Empty the Deck; must be first line of function
        
        full_deck = Deck()
        full_deck.new_pack(jokers=randint(0,2))

        self.data = sample(full_deck, randint(0,len(full_deck)))
    
    def discard_random(self, count=1):
        '''Discard [count] random cards.'''
        for _ in range(count):
            self.data.remove(choice(self.data))
            
    def deal(self, hand, count=1):
        '''Deal from the Deck into the hand'''
        hand += self.draw(count)

    def place_bottom(self, cards):
        '''Place cards on the bottom of the deck. Works with individual Card
        and lists of Card.'''
        if not isinstance(cards, list):
            cards = [cards]
        self.data += cards

    def place_top(self, cards):
        '''Place cards on the top of the deck. Works with individual Card
        and lists of Card.'''
        if not isinstance(cards, list):
            cards = [cards]
        self.data = cards + self.data

    def draw(self, count=1):
        '''Draw cards from the top of the Deck. Returns a list'''
        cards = self.data[:count]
        self.data = self.data[count:]
        return cards

    def rotate(self, count=1):
        '''Rotate a card from the top of the deck to the bottom of the deck.'''
        cards = self.draw(count)
        self.place_bottom(cards)

    def peek_top(self, count=1):
        '''Look at cards off the top of the deck.'''
        return self.data[:count]

    def peek_bottom(self, count=1):
        '''Look at cards off the top of the deck.'''
        return self.data[-count:]

    #TODO
    def sort(self):
        '''Sorts the cards in the order of Suit, then Value. Jokers first
        overall.'''
        pass
    
    def shuffle(self):
        '''Shuffle the Deck using random.shuffle().'''
        shuffle(self.data)

    #TODO: test
    def shuffle_piles(self, pile_count=5):
        '''Shuffle by drawing cards and putting them in separate piles'''
        new_deck = []
        for pile_number in pile_count:
            new_deck += self.data[::pile_number]

        self.data = new_deck

    def cut(self, weights):
        '''Cut the deck, return the cuts as list elements. Each slice is given an
        integer weight, in order, from the list `weights`.  The slices are
        returned in the order of their weight. This means that a simple [1,0,2]
        will work, as will [2,1,3], as will [0, -765, 100000].'''
        if len(weights) > len(self):
            raise IndexError('There are more slices to your cut than there are cards')

        #https://stackoverflow.com/a/7851166
        positions = sorted(range(len(weights)), key=lambda k: weights[k])

        large_cut_size = ceil(len(self.data) / len(positions))
        small_cut_size = floor(len(self.data) / len(positions))

        deck_cuts = []
        #Break the deck into optimally smooth cuts
        position = 0
        remaining_cuts = len(weights)

        # The optimally smooth cut can be found with an iterative algorithm
        #  1) Take all the large cuts until you can fill the rest with small cuts
        #     Detect this with: (cards - position) % (small * remaining_cuts) == 0
        #  2) Take all the small cuts
        #
        # A worked example:
        # 13 cards, 5 cuts (large cut: 3, small cut: 2)
        #
        # (13 - 0) % (2 * 5) = 3 (take a large slice of 3, position+=3, cuts-=1)
        # (13 - 3) % (2 * 4) = 2 (take a large slice of 3, position+=3, cuts-=1)
        # (13 - 6) % (2 * 3) = 1 (take a large slice of 3, position+=3, cuts-=1)
        # (13 - 9) % (2 * 2) = 0 (It equals 0, so the rest are small cuts.)
        # There are 2 more cuts until we hit our target.
        #
        # 3 large cuts * 3 cards + 2 small cuts * 2 cards = 9 + 4 = 13. Correct.
        # 
        # Note that the modulo sequence 3,2,1,0 in this example is a coincidence.
        while (len(self.data) - position) % (small_cut_size * remaining_cuts) != 0:
            deck_cuts.append(self.data[position:position+large_cut_size])
            position += large_cut_size
            remaining_cuts -= 1
        while position <= len(self.data):
            deck_cuts.append(self.data[position:position+small_cut_size])
            position += small_cut_size
        

        #Sort those cuts into the order they need to be for returning
        #print(len(deck_cuts), len(positions))
        ordered_cuts = [deck_cuts[p] for p in positions]

        return ordered_cuts

    def shuffle_cut(self, weights):
        '''Shuffle the deck by cutting the cards, replacing the cuts in the
        order of their weights as determined by the cut() function'''
        new_deck = []
        for cuts in self.cut(weights):
            new_deck += cuts

        self.data = new_deck

class Hand(Deck):
    '''An alias for the Deck class that allows you to differentiate hands by
    type.'''
    def __init__(self, cards=[]):
        self.data = cards

if __name__ == '__main__':
    d0 = Deck()
    d0.new_pack()
    d = Deck(d0[:])

    c = d.cut([1,2,3,4,5,6])
    for i, cut in enumerate(c):

        for j, card in enumerate(cut):
            #print(type(card))
            print(card.unicard(), end='|')
        print(end=' ')
    print()
    
    c = d.cut([6,5,4,3,2,1])
    for i, cut in enumerate(c):

        for j, card in enumerate(cut):
            #print(type(card))
            print(card.unicard(), end='|')
        print(end=' ')
    print()
    
