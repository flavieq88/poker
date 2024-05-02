#identification section

#file for the computer bot

from players import Player
from random import shuffle, randint
from table import *
from winninghand import *


def handstrength(pocketcards, community, n_iter=1000, n_samples=10):
    """Returns the hand strength of current hand and community cards
    input parameters: pocketcards is a list of 2 cards
    Community is the list of community cards from PockerGame, so could contain None"""
    
    #preprocess and remove all the Nones if there are for it to work correctly
    temp = community.copy()
    for i in range(len(community)): 
        if community[i] is None:
            temp = community[:i] #stop right before
            break

    missing = 7 - len(temp) #max is 7 unknowns, min will be 2 unknowns
    d = [Card(i,j, True) for j in ["Club", "Diamond", "Heart", "Spade"] 
                     for i in range(2, 15)] #create a full deck
    for card in pocketcards+temp:
        d.remove(card) #remove the already known cards from the deck
    h= 0 #for total hand strength
    for i in range(n_samples):
        wins = 0
        for j in range(n_iter): #do n_iter random hands
            shuffle(d)
            #build the unknown cards
            rest = d[:missing] # total of n_missing cards chosen at random (shuffled)
            opponent = rest[:2] # for sure 2 cards for opponent pocket cards
            total_community = temp+rest[2:] #rest of the cards are the rest of community cards
            if getwinner(pocketcards+total_community, opponent+total_community) != "Loss":
                wins += 1
        P = wins/n_iter
        h += P
    return h/n_samples #average                     
#detailed testing and analysis for handstrength and the concept of sampling can be found in testing_handstrength.py and testing_handstrength_analysis.txt
#note: i tried using my class Deck instead of a list for the deck in this function, but it was significantly slower 
#and since it is meant to iterate so many times, I decided to just use the faster approach


class Bot(Player): #inherit from Player

    def __init__(self, difficulty="EASY", pocket = [None, None], money = 500):
        super().__init__(pocket, money)
        self.difficulty = difficulty #string, either EASY, MEDIUM, HARD (determined by user choice in GUI)

    def potodds(self, game):
        current = game.pot
        needed = game.players[0].lastbet - self.lastbet # amount needed to put in to call/raise the bet
        return needed/(current+needed)

    
    def doAction(self, game): #game is a PokerGame object (the current one)
        """Makes the computer pick a move depending on the strategy (difficulty level)"""
        if self.difficulty == "EASY":
            self.random_strat(game)
        elif self.difficulty == "MEDIUM":
            self.passive_loose(game)
        else: # hard
            self.aggressive_tight(game)

    def random_strat(self, game):
        """Makes the computer do an action by picking randomly an action"""
        pass

    def passive_loose(self, game):
        """Computer makes a move with a passive-loose strategy"""

    def aggressive_tight(self, game):
        """Computer makes a move with an aggresive-tight strategy"""
        h = handstrength(self.pocket, game.community) #handstrength
        p = self.potodds(game)
        