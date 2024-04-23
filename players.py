#identification section


class Player(object):
    def __init__(self, pocket = [], money = 500): 
        self.pocket = pocket #list of cards
        self.money = money #int
        self.lastbet = 0
        self.totalbet = 0
        self.alive = True #alive in the Game
        self.inPlay = True #in play in a round

    def check(self, game):
        """Returns True if Player check if possible, else returns False"""
        if game.roundpot == 0:
            self.raisebet(0, game)
        

    def raisebet(self, amount, game):
        """Player raises bet to amount, assumes that the amount is legal""" 
        # min raise = raise to double the previous bet, and if previous bet = 0 then shoudl be at least the small blind
        self.lastbet = amount

    def callbet(self, amount):
        """jkjksf"""
    
    def fold(self):
        """Player fold (forfeiting the round)"""
        self.inPlay = False

    def doAction(self):
        """Player does an action"""
        return self.inPlay #if folded, means stop = False
    
"""
table of functions
dict indexed by 

finite state machine 
start hew hand, human turn, computer turn, finish

simon code 
"""