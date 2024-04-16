"""
Flavie Qin 2230509
Programming Techniques and Applications
R. Vincent, instructor
Final Project
"""

#file for the computer bot

from table import *
from winninghand import *

class Bot(Player):

    def __init__(self, difficulty, pocket = [], money = 500):
        super().__init__(pocket = [], money = 500)
        self.difficulty = difficulty

    def handstrength(self, community):
        """Calculated the hand strength of current hand and community cards"""
        pocketcards = self.pocket