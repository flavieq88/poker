#identification section


class Player(object):
    def __init__(self, pocket = [None, None], money = 500): 
        self.pocket = pocket #list of cards
        self.money = money #int
        self.lastbet = 0
        self.totalbet = 0
        self.alive = True #alive in the Game
        self.inPlay = True #in play in a round

    def check(self, game):
        """Modifies all attributes when a player checks"""
        pass
        

    def raisebet(self, amount, game):
        """Player raises bet to amount, assumes that the amount is legal""" 
        # min raise = raise to double the previous bet, and if previous bet = 0 then shoudl be at least the small blind
        pass

    def callbet(self, amount):
        """jkjksf"""
        pass
    
    def fold(self):
        """Player fold (forfeiting the round)"""
        self.inPlay = False
        pass

