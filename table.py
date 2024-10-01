# Class Representation of basic objects for the Poker table (decks, cards)

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
        """Returns a string representing the card. Will be very useful for displaying the images in GUI!"""
        if self.faceUp:
            return str(self.rank)+self.suit
        return "card"
    
    def equal(self, other): #second equal to know if cards are totally the same (same rank and same suit)
        return (self.rank==other.rank and self.suit==other.suit) 

    #establish total ordering between cards:
    #suit doesnt matter in terms of total ordering
    def __eq__(self, other):
        return (self.rank == other.rank)
    
    def __gt__(self, other):
        return (self.rank > other.rank)


class Deck(object):
    def __init__(self, faceUp=False):
        self.deck = [Card(i,j, faceUp) for j in ["Club", "Diamond", "Heart", "Spade"] 
                     for i in range(2, 15)] #standard 52 card deck
    
    def shuffle(self):
        """Shuffles the deck"""
        shuffle(self.deck)
    
    def remove(self, card):
        """Removes the card from the deck"""
        self.deck.remove(card)

    def pop(self, faceUp=True):
        """Removes and returns one card from the deck"""
        p = self.deck.pop()
        p.faceUp = faceUp
        return p
    
    

#Testing code
if __name__ == "__main__":

    #testing class Card and Deck
    AceSpade = Card(14, "Spade", True)
    assert str(AceSpade) == "14Spade"
    AceSpade.flip()
    assert AceSpade.faceUp == False
    assert str(AceSpade) == "card"
    dd = Deck(faceUp = True)
    dd.shuffle()
    print("shuffled deck:", dd.deck)

    d = Deck(faceUp = False)
    assert len(d.deck) == 52
    d.shuffle()
    c = d.pop(faceUp=False)
    assert str(c) == "card"
    c.flip()
    print(c)
    TwoClub = Card(2, "Club")
    assert TwoClub <= AceSpade
    assert not TwoClub.equal(AceSpade)
    assert Card(3, "Club").equal(Card(3, "Club"))
    assert not Card(3, "Heart").equal(Card(3, "Club"))
    d.remove(Card(4, "Spade"))
    print("All tests passed")

 
    
    