#identification section

from table import *
from players import *

class PokerGame(object):

    def __init__(self, human, computer, smallblind=5, bigblind=10):
        self.totalpot = 0
        self.roundnumber = 0 # round number = 0:preflop, 1:flop, 2:turn, 3:river
        self.player1 = human #Player object
        self.player2 = computer #Bot object
        self.smallblind = smallblind #value of small blind
        self.bigblind = bigblind #vlaue of big blind
        self.community = [] #list of community cards
        self.deck = Deck() #create a standard deck
        while self.gameOngoing(): #continue new rounds until someone dies
            self.startGame()
    
    def givePocketCards(self):
        """Distributes pocket cards to both players"""
        for _ in range(2):
            self.player1.hand.append(self.deck.pop())
            self.player2.hand.append(self.deck.pop())

    def gameOngoing(self):
        """Returns True if both players are still alive, False otherwise"""
        return (self.player1.alive and self.player2.alive)
    
    def newGame(self):
        """Reinitializes stuff when a new game starts"""
        self.totalpot = 0
        self.community = []

    def givePot(self):
        """Gives the pot to the player who won (or splits if a tie)"""
        
    
    def startGame(self):
        """Starts a new round"""
        self.deck.shuffle()
        self.givePocketCards()
        
# i define one game to be a full game
# and one round to be each time theres a new betting round
# a betting round ends when a player1.called this round == pleyer2.called this round
