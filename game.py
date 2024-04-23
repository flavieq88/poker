#identification section

from table import *
from players import *

class PokerGame(object):

    def __init__(self, human, computer, smallblind=5, bigblind=10):
        self.totalpot = 0
        self.phase = 0 # phase = 0:preflop, 1:flop, 2:turn, 3:river
        self.players = (human, computer) #tuple of players (Player, Bot) objects
        self.smallblind = smallblind #value of small blind
        self.bigblind = bigblind #vlaue of big blind
        self.smallblindplayer = 1 #number corresponds to index in the list of players. 
                                  #setting initial smallblindplayer = 1 so that in every new game it boots up, human will be first
        self.community = [] #list of community cards
        self.deck = None #place to store the deck
    
    def givePocketCards(self):
        """Distributes pocket cards to both players"""
        for _ in range(2):
            playercard = self.deck.pop()
            playercard.faceUp = True #make card visible to the user
            self.players[0].hand.append(playercard) #give to human (user)
            self.players[1].hand.append(self.deck.pop()) #opponent's cards are not visible to user

    def gameOngoing(self):
        """Returns True if both players are still alive, False otherwise"""
        return (self.player1.alive and self.player2.alive)
    
    def newRound(self):
        """Reinitializes stuff when a new round starts"""
        self.totalpot = 0 #restart the community pot
        self.community = [] #empty the community pile
        self.deck = Deck().shuffle() #with a new, full deck and shuffled
        self.smallblindplayer = (self.smallblindplayer+1)%2 #switch the small blind and big blind players
    
    def betting(self):
        while self.players[0].lastbet == self.players[1].lastbet and : #continue until the players matched each other in bet
            if playerSB.doAction() == True:
                #does stuff
            =
        return all(self.players, key = lambda x: x.inPlay) #will return True if all players wish to continue, False otherwise
    
    def preflop(self):
        """Does the stuff in a preflop phase"""
        #distribute pocket cards
        # start betting (wiht the small blind player who starts)
        return True
    
    def flop(self):
        return 
    
    def turnriver(self):
        """Same process for turn or river"""
        return 
    
    def showdown(self):
        """Does the stuff if we get to a showdown"""
        #reveal cards
        #determine winner
        #distribute pot
        return
    
    def givePot(self):
        """Gives the pot to the player who won (or splits pot if a tie)"""
        # if one winner: then 
        return 
    
    def startRound(self):
        """Starts a new round (will last until a player wins the pot)"""
        if not self.preflop(): # if it returns False = round ended there
            return
        # if self.preflop() == something, break so that it does all the action but returns something if not
            # preflop phase
            # postflop phase
            # turn phase
            # river phase
            # showdown
            #if at any point one person .inPlay = False, that means they folded so return so the round ends there

    def startGame(self):
        """Starts a new game (will last until a player lost all their money)"""
        while self.gameOngoing(): #contiue until one player loses
            self.newRound() #reinitilize stuff for new round
            self.startRound()
        
# i define one game to be a full game (until one player runs out of money)
# and one round to be each time theres new pocket cards distributed
# a betting round ends when a player1.called this round == pleyer2.called this round
# and a phase = each time theres a betting phase (ie: preflop, flop, turn, river)
