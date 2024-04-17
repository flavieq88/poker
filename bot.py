"""
Flavie Qin 2230509
Programming Techniques and Applications
R. Vincent, instructor
Final Project
"""

#file for the computer bot

from players import Player
from table import *
from winninghand import *

def handstrength(self, community, n_iter=1000, n_samples=10):
        """Returns the hand strength of current hand and community cards"""
        pocketcards = self.pocket
        missing = 7 - len(community)
        deck = Deck() #create a full deck
        for card in pocketcards+community:
            deck.delete(card) #remove the known cards from the deck
        rest = []
        average = 0
        for i in range(n_samples): #repeat the sampling n_samples times
            wins = 0
            for i in range(n_iter): #do n_iter random hands
                for i in range(missing): #build the unknown cards
                    rest.append(deck.getcard()) #get random cards
                opponent = rest[:2] # for sure 2 cards for oppinent pocket cards
                community += rest[2:] #rest of the cards are the rest of community cards
                if getwinner(pocketcards+community, opponent+community) != "Loss":
                     wins += 1
            P = wins/n_iter
            average += P
        average = average/n_samples
        return average
                            
#testing for handstrength in testing_sampling.py

class Bot(Player):

    def __init__(self, difficulty, pocket = [], money = 500):
        super().__init__(pocket = [], money = 500)
        self.difficulty = difficulty

    