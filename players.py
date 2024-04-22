#identification section


class Player(object):
    def __init__(self, pocket = [], money = 500, smallblind = True): 
        self.pocket = pocket #list of cards
        self.money = money #int
        self.lastbet = 0
        self.smallblind = smallblind
        self.alive = True


    def check(self, game):
        """Returns True if Player check if possible, else returns False"""
        if game.roundpot == 0:
            return True

    def raisebet(self, amount, game):
        """Player raises bet to amount""" 
        # min raise = raise to double the previous bet, and if previous bet = 0 then shoudl be at least the small blind

    def callbet(self, amount):
        """jkjksf"""
    
    def fold(self):
        self.alive = False
