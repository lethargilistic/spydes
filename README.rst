Spydes
------

Python3-exclusive playing cards in four suits, with and without
jokers.

It's time to let go of Legacy Python, but I'm not about to rip it out of someone
else's project. I'm not a jerk.

How to use it
-------------
Card
~~~~
A `Card` is a namedtuple with extensions for printing out to the screen.
The tuple has two values, `Suit` and `Value`, which are intended to take their
values from the enumerators documented elsewhere. However, strictly speaking,
you're not required to use the enumerators. The pretty output extensions would
no longer work, but you could redefine `__str__` or use `__repr__` for
debugging if you want custom suits or values.

__str__()
_________
Outputs two characters, representing the value and the suit. For
example, "TC" would represent the 10 of Clubs and "AS" would represent the Ace
of Spades (salute!).

unicard(vary_jokers=False)
_______
Returns the Unicode character representing that playing card, using the
`unicard` library. It also handles Jokers, which `unicard` does not.

There are 3 Unicode Joker characters, but the default is `🃏`. If you would like
to use more than one, you may set `vary_jokers` to `True`. The Jokers are
differentiated by their Value, modulo 3.

Deck
~~~~
You can instantiate a Deck() from which to draw(), cut(\*weights), or
shuffle().

Hand
~~~~
A `Hand` is literally a `Deck`. It's an alias. It exists so that you can write more
natural lines like:
.. code-block:: python
   deck = Deck()
   player_one_hand = Hand() #not Deck()
   player_two_hand = Hand() #not Deck()

Suit
~~~~
An enumerator for the playing card Suit that includes the standard four as `CLUB`,
`SPADE`, `DIAMOND`, and `HEART`. In addition, it also allows you to mark Jokers with
`JOKER`.

standard_suits
______________
For your convenience, spydes also provides a list called `standard_suits` that
includes only the four suits, without the Joker. You may iterate through this if
you want to do some aggregate operation with just the suits.

.. code-block:: python
    >>> for suit in standard_suits:
    ...   print(suit)
    ... 
    Suit.CLUB
    Suit.SPADE
    Suit.DIAMOND
    Suit.HEART


Value
~~~~~
An enumerator for the playing card Suit that includes the thirteen standard
values by name.


standard_values
_______________
For your convenience, spydes also provides a list called `standard_values`. You
can iterate through it to get all the suits, in numerical order. It mostly
exists for consistency with `standard_suits`


How to license it
-----------------
MIT License
