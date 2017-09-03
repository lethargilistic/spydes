from collections import namedtuple, UserList
from enum import Enum, unique
from math import ceil, floor
from random import choice, randint, sample, shuffle
from unicards import unicard

class Suit(Enum):
    JOKER = "*"
    SPADE = "S"
    HEART = "H"
    DIAMOND = "D"
    CLUB = "C"

    WILDCARD = "*"
    PAGLIACCI = "*"
    OLD_MAID = "*"
    TRUMP_CARD = "*"
    BEST_BOWER = "*"
    THE_FOOL = "*"
    THE_FLY = "*"
    THE_BIRD = "*"

    LEAF = "S"
    SHIELD = "S" 
    
    ROSE = "H" 

    TILE = "D"
    BELL = "D"

    ACORN = "C"

all_suits = [Suit.SPADE, Suit.HEART, Suit.DIAMOND, Suit.CLUB]
red_suits = [Suit.HEART, Suit.DIAMOND]
black_suits = [Suit.SPADE, Suit.CLUB]

class Value(Enum):
    ACE = 1
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

    A = 1
    ALAS = 1
    BULL = 1
    BULLET = 1
    EYES = 1
    MASTERCARD = 1
    ONE_SPOT = 1
    ROCKET = 1
    SEED = 1
    SPIKE = 1
    SPOT = 1

    DEUCE = 2
    DEWEY = 2
    DUCK = 2
    SWAN = 2

    CRAB = 3
    BUTTS = 3
    TREY = 3

    BOAT = 4
    FOUR_SPOT = 4
    ONE_LEGGED_ACE = 4
    BROKEN_ACE = 4
    SAILBOAT = 4
    
    FIVE_SPOT = 5
    NICKEL = 5
    PEDRO = 5
    FEVER = 5

    BOOT = 6
    SAX = 6
    SEX = 6

    CANDY_CANE = 7
    HOCKEY_STICK = 7
    MULLET = 7
    SALMON = 7
    WALKING_STICK = 7

    FAT_LADY = 8
    OCHO = 8
    SNOWMAN = 8
    EIGHT_LAND = 8
    RACE_TRACK = 8
    TIME_TRAVEL = 8
    HOG_NADS = 8

    NEENER = 9
    NINA_ROSS = 9
    NINER = 9
    POTHOOK = 9

    T = 10
    DIME = 10
    SAWBUCK = 10
    BO_DEREK = 10

    J = 11
    BOY = 11
    BOWER = 11
    FISHHOOK = 11
    HOOK = 11
    J_BIRD = 11
    J_BOY = 11
    JACKAL = 11
    JACKSON = 11
    JACKSONVILLE = 11
    JAKE = 11
    JOHN = 11
    JOHNNY = 11
    JOHNSON = 11
    KNAVE = 11
    VALET = 11

    Q = 12
    COWGIRL = 12
    DAME = 12
    LADY = 12
    GIRL = 12
    HEN = 12
    JOY_GIRL = 12
    PAINTED_LADY = 12
    MOP_SQUEEZER = 12
    STENOGRAPHER = 12

    K = 13
    COWBOY = 13
    K_BOY = 13
    MONARCH = 13
    SERGEANT = 13

all_values = [Value(rank) for rank in range(1,14)]
face_values = [Value.KING, Value.QUEEN, Value.JACK]
broadway_values = [Value.ACE, Value.KING, Value.QUEEN, Value.JACK, Value.TEN]
number_values = [Value(rank) for rank in range(1,11)]

class Card(namedtuple('Card', ['Suit', 'Value'])):
    def __str__(self):
        output = "_A23456789TJQK"[self.Value.value]
        output += self.Suit.value
        return output
    
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
                return "_🃏🃟🂿"[self.Value.value%3+1] #%3+1 guarantees list bounds
            else:
                return "🃏"

        return unicard("_A23456789TJQK"[self.Value.value] + self.Suit.value.lower())

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
                self.data.append(Card(Suit.JOKER, Value(number%3+1)))

            for suit in standard_suits:
                for value in standard_values:
                    self.data.append(Card(suit, value))

    def fill_suit(self, suit, count=1):
        '''Add all cards of a suit. Count is the number of times you want to add
        all the cards from that suit. You may use Suit.JOKER to get one Joker.'''
        for num in range(count):
            if suit == Suit.JOKER:
               self.data.append(Card(Suit.JOKER, Value(num%3+1)))
            else:
                for value in Value:
                    self.data.append(Card(suit, value))

    def fill_value(self, value, count=1):
        '''Add all cards of a value. No Jokers. If you want to add jokers
        similarly, use fill_suit()'''
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
        # 3 large cuts of 3 cards + 2 small cuts of 2 cards = 9 + 4 = 13. Correct!
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
        return [deck_cuts[p] for p in positions]

    def shuffle_cut(self, weights):
        '''Shuffle the deck by cutting the cards, replacing the cuts in the
        order of their weights as determined by the cut() function'''
        new_deck = []
        for cuts in self.cut(weights):
            new_deck += cuts

        self.data = new_deck

    def unicard(self, vary_jokers=False):
        '''Display all cards in Deck as unicode cards'''
        output = ""
        for card in self.data:
            output += card.unicard() + ' '
        return output

class Hand(Deck):
    '''An alias for the Deck class that allows you to differentiate hands by
    type.'''
    def __init__(self, cards=[]):
        self.data = cards

if __name__ == '__main__':
    d = Deck()
    d.fill_suit(Suit.SPADE)
    d.fill_suit(Suit.DIAMOND, 2)
    d.fill_suit(Suit.JOKER, 6)
    print(d.unicard())
