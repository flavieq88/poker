#identification section


class Player(object):
    def __init__(self, pocket = [None, None], money = 500): 
        self.pocket = pocket #list of cards
        self.balance = money # int value of current balance
        self.lastbet = 0 # last bet made in a round
        self.totalbet = 0
        self.alive = True #alive in the Game
        self.inPlay = True #still alive/in play in a round
        self.did_action = False #to keep track if they did an action in a pphase (for checking if agree)

    # the following methods are for a certain action is taken. always assumes it is legal to do that action 
    def check(self):
        """Modifies all required attributes for when a player checks"""
        print("check")
        self.did_action = True
        return # do nothing!

    def raisebet(self, other, amount):
        """Modifies all required attributes when Player raises bet to amount, assumes that the amount is legal""" 
        # min raise = raise to double the previous bet, and if previous bet = 0 then shoudl be at least the small blind
        self.totalbet = self.totalbet - self.lastbet + amount #must subtract the previous last bet of the round before adding since its raising the bet to (cumulatively)
        self.balance = self.balance + self.lastbet - amount # again must take into account lastbet is "cumulative" bet
        self.lastbet = amount # update the new lastbet
        raisedamount = amount - other.lastbet
        print("raised")
        self.did_action = True
        return raisedamount

    def callbet(self, amount):
        """Modifies all required attributes when a player calls to the amount"""
        self.totalbet = self.totalbet - self.lastbet + amount #must subtract the previous last bet of the round before adding since its raising the bet to (cumulatively)
        self.balance = self.balance + self.lastbet - amount # again must take into account lastbet is "cumulative" bet
        self.lastbet = amount # update the new lastbet
        self.did_action = True
        print("called")
    
    def fold(self):
        """Modifies all attributes when a Player folds (forfeits the round)"""
        self.inPlay = False
        self.did_action = True
        print("folded")
        

   

