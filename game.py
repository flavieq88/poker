#identification section

from table import *

class PokerGame(object):

    def __init__(self, human, computer, smallblind=5, bigblind=10):
        self.totalpot = 0
        self.roundnumber = 0 # round number = 0:preflop, 1:flop, 2:turn, 3:river
        self.player1 = human #Player object
        self.player2 = computer #Bot object
        self.roundpot = 0
        self.smallblind = smallblind
        self.bigblind = bigblind
        self.community = [] #list of community cards
        self.deck = Deck()
        while self.gameOngoing(): #continue new rounds until someone dies
            self.startRound()
    
    def givecards(self):
        """Distributes pocket cards for both players"""
        for i in range(2):
            self.player1.hand.append(self.deck.pop())
            self.player2.hand.append(self.deck.pop())

    def gameOngoing(self):
        """Returns True if both players are still alive, False otherwise"""
        return (self.player1.alive and self.player2.alive)

    def startRound(self):
        """Starts a new round"""
        self.deck.shuffle()