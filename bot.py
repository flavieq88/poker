"""
Flavie Qin 2230509
Programming Techniques and Applications
R. Vincent, instructor
Final Project
"""

#file for the computer bot

from players import Player
from random import shuffle
from table import *
from winninghand import *

def handstrength(pocketcards, community, n_iter=1000, n_samples=10):
    """Returns the hand strength of current hand and community cards"""
    missing = 7 - len(community) #max is 7 unknowns, min will be 2 unknowns
    deck = [Card(i,j) for j in ["Club", "Diamond", "Heart", "Spade"] 
                     for i in range(2, 15)] #create a full deck
    for card in pocketcards+community:
        deck.remove(card) #remove the already known cards from the deck
    average = 0
    for i in range(n_samples): #repeat the sampling n_samples times
        wins = 0
        for j in range(n_iter): #do n_iter random hands
            rest = []
            shuffle(deck)
            #build the unknown cards
            rest = deck[:missing]
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

    