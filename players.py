#identification section


class Player(object):
    def __init__(self, pocket = [None, None], money = 500): 
        self.pocket = pocket #list of cards
        self.money = money #int value of starting balance
        self.balance = money # int value of current balance
        self.lastbet = 0 # last bet made in a round
        self.totalbet = 0
        self.alive = True #alive in the Game
        self.inPlay = True #still alive/in play in a round

    def check(self):
        """Modifies all required attributes for when a player checks"""
        pass # do nothing

    def raisebet(self, amount):
        """Modifies all required attributes when Player raises bet to amount, assumes that the amount is legal""" 
        # min raise = raise to double the previous bet, and if previous bet = 0 then shoudl be at least the small blind
        self.totalbet = self.totalbet - self.lastbet + amount #must subtract the previous last bet of the round before adding since its raising the bet to (cumulatively)
        self.balance = self.money - self.totalbet
        self.lastbet = amount
        

    def callbet(self, amount):
        """Modifies all required attributes when a player calls the amount"""
        self.totalbet = self.totalbet - self.lastbet + amount
        self.balance = self.money - self.totalbet
        self.lastbet = amount
    
    def fold(self):
        """Modifies all attributes when a Player folds (forfeits the round)"""
        self.inPlay = False
        

   

