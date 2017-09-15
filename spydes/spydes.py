from collections import namedtuple, UserList
from enum import Enum, unique
from math import ceil, floor
from random import choice, randint, sample, shuffle
from unicards import unicard

#pytest says to have a dot. Me running this program says to not have a dot.
#Eventually(TODO), I'll remove the no dot version, but I'm still rapid
#prototyping right now
try:
    from .card_enum import Suit, Value
except ModuleNotFoundError:
    from card_enum import Suit, Value

all_suits = [Suit.spade, Suit.heart, Suit.diamond, Suit.club]
red_suits = [Suit.heart, Suit.diamond]
black_suits = [Suit.spade, Suit.club]

all_values = [Value(rank) for rank in range(1,14)]
face_values = [Value.king, Value.queen, Value.jack]
broadway_values = [Value.ace, Value.king, Value.queen, Value.jack, Value.ten]
number_values = [Value(rank) for rank in range(1,11)]

class Card(namedtuple('Card', ['Suit', 'Value'])):
    def __str__(self):
        output = "_A23456789TJQK"[self.Value.value]
        output += self.Suit.value
        return output
    
    def same_suit(self, card):
        '''Does card have the same suit as self?'''
        return self.Suit == card.Suit

    def same_value(self, card):
        '''Does card have the same value as self? All Jokers are equivalent,
        regardless of value.'''
        both_jokers = self.Suit == Suit.joker and card.Suit == Suit.joker
        either_jokers = self.Suit == Suit.joker or card.Suit == Suit.joker

        #If both are jokers, they are equivalent
        if both_jokers:
            return True

        #If one is a joker, but not both, they are different.
        if either_jokers:
            return False
        
        #Because neither are Jokers, just compare value
        return self.Value == card.Value

    def unicard(self, vary_jokers=False, color=False):
        '''Returns a Unicode card representation of the card.

        If vary_jokers is True, then all three Unicode jokers may be
        represented. The Value of a joker card (1,2,3) determines which is
        shown.
        
        If vary_jokers is False, then all jokers will look like the 1 joker
        card. That 1 joker is one most likely to work correctly in
        terminals, assuming not all are supported properly.
        
        If you set color to True, the cards will be converted to color in
        terminals.'''
        if self.Suit == Suit.joker:
            if vary_jokers:
                return "_🃏🃟🂿"[self.Value.value%3+1] #%3+1 guarantees list bounds
            else:
                return "🃏"

        return unicard("_A23456789TJQK"[self.Value.value]
                        + self.Suit.name[0].lower(), color=color)

    def unicard_back():
        '''Return a facedown card Unicode string'''
        return unicard('b')

class Deck(UserList):
    def __init__(self, cards=[]):
        self.data = cards
    
    def __str__(self):
        output = '[' + str(self.data[0])
        for card in self.data[1:]:
            output += ', ' + str(card)
        return output + ']'

    def new_pack(self, packs=1, jokers=0):
        '''Fill the Deck with a new, complete set of playing card with the
        number of jokers desired'''
        self.clear() #Empty the Deck; must be first line of function

        for each_pack in range(packs):
            for number in range(jokers):
                #%3+1 puts Joker within the range of the three Unicode jokers
                self.data.append(Card(Suit.joker, Value(number%3+1)))

            for suit in all_suits:
                for value in all_values:
                    self.data.append(Card(suit, value))

    def fill_suit(self, suits, count=1):
        '''Add all cards of a suit. Count is the number of times you want to add
        all the cards from that suit. You may use Suit.joker to get one Joker.'''
        suits = suits if isinstance(suits, list) else [suits]

        for suit in suits:
            for num in range(count):
                if suit == Suit.joker:
                   self.data.append(Card(Suit.joker, Value(num%3+1)))
                else:
                    for value in Value:
                        self.data.append(Card(suit, value))

    def fill_value(self, values, count=1):
        '''Add all cards of a value. No Jokers. If you want to add jokers
        similarly, use fill_suit()'''
        values = values if isinstance(values, list) else [values]
        
        for value in values:
            for _ in range(count):
                for suit in Suit:
                    self.data.append(Card(suit, value))

    def found_pack(self):
        '''I found this abandoned pack of playing cards at the library. It's
        probably not complete... But what if it is...? Oh, wow. Who cares? Look
        at the design on the back! I'm keeping these.'''
        self.clear() #Empty the Deck; must be first line of function
        
        full_deck = Deck()
        full_deck.new_pack(jokers=randint(0,2))

        self.data = sample(full_deck, randint(0,len(full_deck)))
    
    def discard_suit(self, suit):
        '''Discard all cards of the suit, return as list'''
        discard_pile = []
        for card in self.data:
            if card.suit == suit:
                self.data.remove(card)
                discard_pile.append(card)
        return discard_pile


    def discard_value(self, value):
        '''Discard all cards of the value, return as list. Jokers are treated as
        a suit, so you cannot discard jokers with this method.'''
        discard_pile = []
        for card in self.data:
            if card.value == value and card.suit != Suit.joker:
                self.data.remove(card)
                discard_pile.append(card)
        return discard_pile

    def discard_random(self, count=1):
        '''Discard [count] random cards.'''
        discard_pile = []
        for _ in range(count):
            discard_pile.append(self.data.remove(choice(self.data)))
        return discard_pile
            
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
        cards = cards if isinstance(cards, list) else [cards]
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

    #FIXME: If there are any jokers in the deck, this breaks
    #Just remove all jokers and count how many there were, add to front?
    def sort(self):
        '''Sorts the cards in the order of Suit, then Value. Jokers first
        overall.'''
        self.data = sorted(self.data, key=lambda card: (card.Suit, card.Value))
    
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
        '''Cut the deck, return the cuts as list elements. Each cut is given an
        integer weight, in order, from the list `weights`.  The cut are
        returned in the order of their weight. This means that a simple [1,0,2]
        will work, as will [2,1,3], as will [0, -765, 100000].'''
        if len(weights) > len(self):
            raise IndexError('There are more cuts than there are cards')

        #https://stackoverflow.com/a/7851166
        positions = sorted(range(len(weights)), key=lambda k: weights[k])

        large_cut_size = ceil(len(self.data) / len(positions))
        small_cut_size = floor(len(self.data) / len(positions))

        # The optimally smooth cut can be found with an iterative algorithm
        #  1) Take all the large cuts until you can fill the rest with small cuts
        #     Detect this with: (cards - position) % (small * remaining_cuts) == 0
        #  2) Take all the small cuts
        #
        # A worked example:
        # 13 cards, 5 cuts (large cut: 3, small cut: 2)
        #
        # (13 - 0) % (2 * 5) = 3 (take a large cut of 3, position+=3, cuts-=1)
        # (13 - 3) % (2 * 4) = 2 (take a large cut of 3, position+=3, cuts-=1)
        # (13 - 6) % (2 * 3) = 1 (take a large cut of 3, position+=3, cuts-=1)
        # (13 - 9) % (2 * 2) = 0 (It equals 0, so the rest are small cuts.)
        # There are 2 more cuts until we hit our target.
        #
        # 3 large cuts of 3 cards + 2 small cuts of 2 cards = 9 + 4 = 13. Correct!
        # 
        # Note that the modulo sequence 3,2,1,0 in this example is a coincidence.
        deck_cuts = []
        position = 0
        remaining_cuts = len(weights)
        
        while (len(self.data) - position) % (small_cut_size * remaining_cuts) != 0:
            deck_cuts.append(self.data[position:position+large_cut_size])
            position += large_cut_size
            remaining_cuts -= 1
        while position <= len(self.data):
            deck_cuts.append(self.data[position:position+small_cut_size])
            position += small_cut_size
        

        #Sort those cuts into the order they need to be for returning
        return [deck_cuts[p] for p in positions]

    def shuffle_cut(self, weights):
        '''Shuffle the deck by cutting the cards, replacing the cuts in the
        order of their weights as determined by the cut() function'''
        new_deck = []
        for cuts in self.cut(weights):
            new_deck += cuts

        self.data = new_deck

    def unicard(self, vary_jokers=False, color=False):
        '''Display all cards in Deck as Unicode cards. The arguments will be
        applied to all cards.'''
        output = ""
        for card in self.data:
            output += card.unicard(vary_jokers=vary_jokers, color=color) + ' '
        return output

class Hand(Deck):
    '''An alias for the Deck class that allows you to differentiate hands by
    type.'''
    def __init__(self, cards=[]):
        self.data = cards

if __name__ == '__main__':
    d = Deck()
    d.new_pack(jokers=4)
    d.shuffle()
    print(d.unicard())
    d.sort()
    print(d.unicard())
