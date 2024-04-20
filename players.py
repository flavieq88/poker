#identification section


class Player(object):
    def __init__(self, pocket = [], money = 500): 
        self.pocket = pocket #list of cards
        self.money = money #int
        self.totalbet = 0 
        self.roundbet = 0 
        self.alive = True
        self.smallblind = True


    def check(game):
        """Returns True if Player check if possible, else returns False"""
        if game.roundpot == 0:
            return True

    def raisebet(game, amount):
        """Player raises bet"""

    def callbet(game, amount):
        """jkjksf"""