#file for the computer bot

from players import Player
from random import shuffle, randint
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

    def __init__(self, difficulty="EASY", pocket = [None, None], money = 500):
        super().__init__(pocket, money)
        self.difficulty = difficulty #string, either EASY, MEDIUM, HARD (determined by user choice in GUI)

    def potodds(self, other, pot, threshold):
        """Calculates the pot odds based on the other Player, the curretn pot, and a threshold number for acting on pocket cards"""
        current = pot
        needed = other.lastbet - self.lastbet # amount needed to put in to call/raise the bet
        if current+needed == 0: #will only happen at the bgeinning of a round
            return threshold #helps for only playing pretty good hands initially, and prevent zero division error
        if needed <= 0: #means youre first to act so pot odds are not useful, just return threshold
            return threshold
        return (needed/(current+needed))**(3/4)

    
    def doAction(self, community, other, pot, legalmoves): #game is a PokerGame object (the current one)
        """Makes the computer pick a move depending on the strategy (difficulty level)"""
        #must return so that it returns the aoount raised to if it does
        if self.difficulty == "EASY":
            return self.random_strat(other, legalmoves)
        elif self.difficulty == "MEDIUM":
            return self.passive_loose(community, other, pot, legalmoves)
        else: # HARD
            return self.aggressive_tight(community, other, pot, legalmoves)

    def random_strat(self, other, legalmoves):
        """Makes the computer do an action by picking randomly an action and returns amount raised if raised"""
        number = 0
        if not any(legalmoves): #if all in, then no legal moves
            return #pass
        while True:
            number = randint(0, len(legalmoves)-1) #from 0 to 3 inclusive
            if legalmoves[number]: # as long as it is a legal move (not False) then continue
                break
        if number == 0: #random picked to check
            self.check()
        elif number == 1: #random picked call
            self.callbet(legalmoves[1]) #call the legal amount
        elif number == 2: #random picked raise
            amount = randint(legalmoves[2][0], legalmoves[2][1]) #now pick a random number to raise (within the min and max)
            return self.raisebet(other, amount) #return the amount raised so we can save it
        else: #random picked fold
            if legalmoves[0]: #if check is available, then check
                self.check()
            else: #check not available so just fold
                self.fold()


    def passive_loose(self, community, other, pot, legalmoves):
        """Computer makes a move with a passive-loose strategy and returns amount raised if raised"""
        threshold = 0.2
        
        h = handstrength(self.pocket, community) #calculate handstrength
        p = self.potodds(other, pot, threshold) #low threshold = still play cards that are not very good at beginning
        
        if h < p: #really bad set of cards, either fold or check if possible
            if legalmoves[0]: #check is available
                self.check()
                return
            else: 
                self.fold()
                return
        else: #h >= threshold
            if (h < 0.6): #card is not good enough, call or check
                if legalmoves[1]:  #call if available: have a higher threshold so it plays tight, more picky
                    self.callbet(legalmoves[1])
                    return
                if legalmoves[0]: #call is not available (first one to bet, and check is available)
                    self.check()
                    return
            elif not legalmoves[2] and h>0.6: #if raise unavailable, then call
                self.callbet(legalmoves[1])
                return

            elif legalmoves[2]: #raise only if card is quite good (>0.6)
                rangeraise = legalmoves[2][1] - legalmoves[2][0] #max raise - min raise
                fifth = rangeraise//5 #int
                if h <0.7: #not as good so raise less
                    amount = randint(legalmoves[2][0], legalmoves[2][0]+fifth) #find a random amount between min raise and halfway 
                    return self.raisebet(other, amount)
                elif h<0.9:
                    amount = randint(legalmoves[2][0]+fifth, legalmoves[2][0]+2*fifth)
                    return self.raisebet(other, amount)
                else: #very good hand strength so raise a lot more
                    amount = randint(legalmoves[2][0]+2*fifth, legalmoves[2][1]) #find a random amount between halfway and max raise
                    return self.raisebet(other, amount)
        #should have returned something by now, but if not, then just check or fold (which is generally always available)
        if legalmoves[0]: #check is available
            self.check()
            return
        self.fold() #if all other actions fail, just fold


    def aggressive_tight(self, community, other, pot, legalmoves):
        """Computer makes a move with an aggresive-tight strategy and retunrs amount raised if raised"""
        threshold = 0.4
        
        h = handstrength(self.pocket, community) #calculate handstrength
        p = self.potodds(other, pot, threshold) #low threshold = still play cards that are not very good at beginning

        if h < p: #really bad set of cards, either fold or check if possible
            if legalmoves[0]: #check is available
                self.check()
                return
            else: 
                self.fold()
                return
        else: #h >= pot odds/threshold
            if (h < 0.5): #not that great of a hand
                if legalmoves[1]:  #call if available: have a higher threshold so it plays tight, more picky
                    self.callbet(legalmoves[1])
                    return
                if legalmoves[0]: #call is not available (first one to bet, and check is available)
                    self.check()
                    return
            elif not legalmoves[2] and h > 0.5: #if raise unavailable, then call
                self.callbet(legalmoves[1])
                return
            elif legalmoves[2]: #raise even if cards are not very good
                rangeraise = legalmoves[2][1] - legalmoves[2][0] #max raise - min raise
                eighth = rangeraise//8 #int
                if h <0.8: #not as good so raise less
                    amount = randint(legalmoves[2][0], legalmoves[2][0]+eighth) #find a random amount between min raise and halfway 
                    return self.raisebet(other, amount)
                elif h<0.9:
                    amount = randint(legalmoves[2][0]+eighth, legalmoves[2][0]+2*eighth)
                    return self.raisebet(other, amount)
                else: #very good hand strength so raise a lot more
                    amount = randint(legalmoves[2][0]+2*eighth, legalmoves[2][1]) #find a random amount between halfway and max raise
                    return self.raisebet(other, amount)
        #should have returned something by now, but if not, then just call or check or fold (which is generally always available)
        if legalmoves[0]: #check is available
            self.check()
            return
        self.fold() #if all other actions fail, just fold
