from table import *

#for determining the winning hand

#functions to determing if a certain rank is present
#they are coded assuming the better ranks have already been deemed not found

def flush(hand):
    """Returns sorted list of all cards in suit forming flush if list of cards hand contains a flush 
    (largest to smallest), False otherwise"""
    d = {}
    for card in hand:
        d[card.suit] = d.get(card.suit, []) + [card]
    for key in d:
        if len(d[key])>=5:
            return sorted(d[key], reverse=True)
    return False

def straight(hand):
    """Returns sorted list of all cards in sequence smallest to largest if list of cards hand contains a straight, 
    False otherwise"""
    #want to include all cards of all suits (including repeats) for other purposes (determining if straight flush), 
    #meaning the list i return could be more than 5 cards
    #ace also can start a straight: ie Ace 2 3 4 5
    #case 1 = normal straight. case 2 = Ace 2 3 4 5... straight

    hand = sorted(hand) # makes a copy too!
    counter = 1
    startingCard = 0 # index of starting card in straight sequence
    for i in range(1, len(hand)):
        if hand[i].rank <= hand[i-1].rank+1: #could either be one rank up or same rank
            counter +=1

        #card doesnt follow but counter is already at 4+, either already a straight or case 2
        #so keep this and if not straight (repeats) no way further in hand a full straight since not enough cards left
        elif counter >=4: 
            break
        else: 
            counter = 1 #restart at this card
            startingCard = i
    #if one, straight sequence will be from starting card to index of startingCard + counter -1
    straightcards = hand[startingCard:startingCard+counter]
    
    #handle possible case 2: if 2 3 4 5 (must start with a 2) and at least up to a 5
    if straightcards[0].rank == 2 and len(straightcards)>=4 and straightcards[-1].rank - 2 >= 3:
        while hand[-1].rank == 14: #check if there are aces at end
            straightcards.insert(0, hand.pop()) 
        if straightcards[0].rank == 14: #valid straight
            return straightcards
    #easy case: for sure no straight
    if len(straightcards)<5:
        return False
    #case 1: valid straight of 5 different ranks min.
    elif len(straightcards)>=5 and straightcards[-1].rank-straightcards[0].rank>=4: 
        return straightcards
    else:
        return False #any other case

def count_ranks(hand):
    """Returns a dictionary with the count of all the ranks in a hand
    Useful for determining 3/4 of a kind, pairs, full house, etc."""
    d = {} #rank:list of cards 
    for card in sorted(hand, reverse=True):
        d[card.rank] = d.get(card.rank, []) + [card]
    return d

def four_kind(d):
    """Using the dictionary returned by count_ranks(hand), if present returns four of a kind cards and kicker, False otherwise"""
    dd = d.copy() # dont want to modify the actual d
    finalHand = []
    for key in dd:
        if len(dd[key])==4:
            finalHand= dd[key]
            del dd[key]
            break
    if finalHand: #not empty = there was a 4 of a kind
        kicker = dd[max(dd)][0] #get kicker, doesnt matter the suit if multiple
        return finalHand + [kicker]
    return False #no 4 of a kind

def three_kind(d):
    """Using the dictionary returned by count_ranks(hand), if present returns list of three of a kind cards, big kicker, small kicker (in this order), False otherwise"""
    dd=d.copy()
    finalHand = []
    for key in sorted(dd, reverse=True): #find biggest ones first
        if len(dd[key])==3:
            finalHand= dd[key]
            del dd[key]
            break
    if finalHand: #not empty = there was a 3 of a kind found
        kicker = dd[max(dd)][:2] #get kicker, list of maximum 2 cards
        del dd[max(dd)] #remove so can get next largest
        if len(kicker)<2: #not enough kickers
            kicker.append(dd[max(dd)][0]) #only one, suit doesnt matter
        return finalHand + kicker
    return False #no 3 of a kind

def two_pairs(d):
    """Using the dictionary returned by count_ranks(hand), if present returns list of largest pair, smaller pair, kicker (in this order), False otherwise"""
    dd = d.copy() #dont want to modify d
    finalHand = []
    n =0 #count number of pairs found
    
    for key in sorted(dd, reverse = True): #so i can find biggest pair first
        if len(dd[key]) == 2:
            finalHand+=dd[key]
            del dd[key]
            n += 1
            if n == 2:
                break
    if len(finalHand) == 4: #have 2 pairs
        kicker = dd[max(dd)][0] #only need 1 kicker
        return finalHand + [kicker]
    #else: no 2 pairs found
    return False

def pair(d): 
    """Using the dictionary returned by count_ranks(hand), if present returns list of pair, big kicker, small kicker (in this order), False otherwise"""
    dd = d.copy()
    finalHand = []
    for key in sorted(dd, reverse=True): #find biggest one first
        if len(dd[key])==2:
            finalHand= dd[key]
            del dd[key]
            break
    if finalHand: #found a pair
        kickers = []
        while len(kickers)<3: #max 3 kickers 
            kickers += dd[max(dd)][:3] 
            del dd[max(dd)]
        kickers = kickers[:3] #only keep 3 kickers
        return finalHand + kickers
    return False

def highcard(hand):
    """Returns the best 5-hand rank, assuming hand only qualifies for high card"""
    hand = sorted(hand, reverse = True)
    return hand[:5] #first 5 elements


#function for finding how good a certain 7-card hand is
def rankHand(hand):
    """Returns a list with first element being the rank from 0(worst)-9(best) of the hand and the final 5-card hand"""
    counts = count_ranks(hand)
    ls = [flush(hand), straight(hand), four_kind(counts), three_kind(counts), two_pairs(counts), pair(counts)]
    if ls[0] and ls[1]:
        #list of elements in both fl and st and of same suit
        sf = []
        for i in ls[1]: #element in straight = keep the ordering
            for j in ls[0]: #each card in flush
                if i.equal(j):
                    sf.append(i)
                    break
    if ls[0] and ls[1] and len(sf)>=5: #straight+flush  
        if sf[-1].rank == 14: #largest is an Ace = royal flush!!!!
            return [9]+sf[-5::][::-1] #only max 5 cards in the case there was 6 cards in the intersection
        else: #straight flush
            return [8]+sf[::-1][:5]
    elif ls[2]: #four of a kind
        return [7]+ls[2]
    elif ls[3] and ls[5]: #full house (three + pair)
        return [6]+ls[3][:3]+ls[5][:2]
    elif ls[0]: #normal flush
        return [5]+ls[0][:5] #five biggest cards 
    elif ls[1]: #normal straight
        temp = {}
        for i in ls[1]:
            temp[i.rank] = i #get rid of duplicate cards of same rank
        new_st = list(temp.values())
        return [4] + new_st[::-1][:5]
        #reverse order so its biggest to smallest (couldnt do sorted in case Ace 2 3 4 5)
    elif ls[3]: # three of a kind
        return [3]+ls[3]
    elif ls[4]: #two pairs
        return [2]+ls[4]
    elif ls[5]: #one pair
        return [1]+ls[5]
    else: #none above categories = high card
        return [0]+highcard(hand)
    

def getwinner(hand1, hand2):
    """Returns "Loss" if hand1 loses, "Tie" if the two hands tie and "Win" if hand1 wins."""
    a = rankHand(hand1)
    b = rankHand(hand2)
    if a>b: #hand1 wins
        return "Win"
    elif a<b: #hand2 wins
        return "Loss"
    else: #tie
        return "Tie"

def category(hand):
    """Returns the string name of the category of the hand"""
    ls = ["high card", "pair", "two pair", "three of a kind", "straight", "flush", "full house", "four of a kind", "straight flush", "royal flush"] 
    #names of categories organized by index returned by rankHand
    rank = rankHand(hand)[0] #get the index number
    return ls[rank]

