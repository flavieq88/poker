"""
Flavie Qin 2230509
Programming Techniques and Applications
R. Vincent, instructor
Final Project
"""

# Representation of the Poker table (decks, cards, etc.)

from random import shuffle
import functools

@functools.total_ordering
class Card(object):
    def __init__(self, rank, suit, faceUp=True):
        self.rank = rank #int
        self.suit = suit #str
        self.faceUp = faceUp #bool
    def flip(self):
        """Flips a card"""
        self.faceUp = not self.faceUp #reverse boolean
    def __repr__(self):
        if self.faceUp:
            return str(self.rank)+self.suit
        return "card"
    
    def equal(self, other): #because eq is only for ranks
        return (self.rank==other.rank and self.suit==other.suit) 

    #establish total ordering between cards:
    #suit doesnt matter in terms of total ordering
    def __eq__(self, other):
        return (self.rank == other.rank)
    def __gt__(self, other):
        return (self.rank > other.rank)


class Deck(object):
    def __init__(self):
        self.deck = [Card(i,j, False) for j in ["Club", "Diamond", "Heart", "Spade"] 
                     for i in range(2, 15)] #standard 52 card deck
    
    def shuffle(self):
        """Shuffles the deck"""
        shuffle(self.deck)

    def _getcard(self):
        """Returns one card from the deck"""
        return self.deck.pop()
    
        
    
class Player(object):
    def __init__(self, pocket = [], money = 500): 
        self.pocket = pocket
        self.money = money
        self.totalbet = 0
        self.roundbet = 0
        self.alive = True


    def check(game):
        """Returns True if Player check if possible, else returns False"""
        if game.roundpot == 0:
            return True

    def raisebet(game, amount):
        """Player raises bet"""

    def callbet(game, amount):
        """jkjksf"""

#Testing code
if __name__ == "__main__":

    #testing class Card and Deck
    AceSpade = Card(14, "Spade", True)
    assert str(AceSpade) == "14Spade"
    AceSpade.flip()
    assert AceSpade.faceUp == False
    assert str(AceSpade) == "card"
    d = Deck()
    assert len(d.deck) == 52
    d.shuffle()
    c = d._getcard()
    c.flip()
    print(c)
    TwoClub = Card(2, "Club")
    assert TwoClub <= AceSpade
    assert not TwoClub.equal(AceSpade)
    assert Card(3, "Club").equal(Card(3, "Club"))
    assert not Card(3, "Heart").equal(Card(3, "Club"))

    print("All tests passed")

 
    
    