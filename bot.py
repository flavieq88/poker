#identification section

#file for the computer bot

from players import Player
from random import shuffle
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

    def __init__(self, difficulty=0, pocket = [None, None], money = 500):
        super().__init__(pocket, money)
        self.difficulty = difficulty #0, 1 or 2 going from easy to hard

    def doAction(self, game): #game is a PokerGame object (the current one)
        """evalutate hand strength and pot odds and decides to do something"""
        h = handstrength(self.pocket, game.community)