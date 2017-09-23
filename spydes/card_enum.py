from enum import Enum

class Suit(Enum):
    joker = 0
    spade = 1
    heart = 2
    diamond = 3
    club = 4

    wildcard = 0
    pagliacci = 0
    old_maid = 0
    trump_card = 0
    best_bower = 0
    the_fool = 0
    the_fly = 0
    the_bird = 0

    leaf = 1
    shield = 1 
    
    rose = 2 

    tile = 3
    bell = 3

    acorn = 4
    clover = 4

    def __lt__(self, other):
        return self.value < other.value

    def ___le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

class Value(Enum):
    ace = 1
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13

    a = 1
    alas = 1
    bull = 1
    bullet = 1
    eye = 1
    mastercard = 1
    one_spot = 1
    rocket = 1
    seed = 1
    spike = 1
    spot = 1

    deuce = 2
    dewey = 2
    duck = 2
    swan = 2

    crab = 3
    butts = 3
    trey = 3

    boat = 4
    four_spot = 4
    one_legged_ace = 4
    broken_ace = 4
    sailboat = 4
    
    five_spot = 5
    nickel = 5
    pedro = 5
    fever = 5

    boot = 6
    sax = 6
    sex = 6

    candy_cane = 7
    hockey_stick = 7
    mullet = 7
    salmon = 7
    walking_stick = 7

    fat_lady = 8
    ocho = 8
    snowman = 8
    eight_land = 8
    race_track = 8
    time_travel = 8
    hog_nads = 8

    neener = 9
    nina_ross = 9
    niner = 9
    pothook = 9

    t = 10
    dime = 10
    sawbuck = 10
    bo_derek = 10

    j = 11
    boy = 11
    bower = 11
    fishhook = 11
    hook = 11
    j_bird = 11
    j_boy = 11
    jackal = 11
    jackson = 11
    jacksonville = 11
    jake = 11
    john = 11
    johnny = 11
    johnson = 11
    knave = 11
    valet = 11

    q = 12
    cowgirl = 12
    dame = 12
    lady = 12
    girl = 12
    hen = 12
    joy_girl = 12
    painted_lady = 12
    mop_squeezer = 12
    stenographer = 12

    k = 13
    cowboy = 13
    k_boy = 13
    monarch = 13
    sergeant = 13

    def __lt__(self, other):
        return self.value < other.value

    def ___le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

