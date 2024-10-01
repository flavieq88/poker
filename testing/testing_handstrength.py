import sys
sys.path[0] = sys.path[0].strip(r"\testing") #go into correct directory

from winninghand import *
from bot import handstrength

from time import perf_counter

# to test if the sampling idea for hand strength is a representative measure of "real" hand strength
# I will use the default for handstrength (10 samples of 1000 iterations each)

# I analyse this data in text file "testing_handstrength_analysis.txt"

# to kind of simulate a real game (just to see the progression of handstrength)
# i will make it calculate handstrength for each round when a new card is placed

#helper function for finding true handstrength
def pocketcombinations(deck):
    """Returns a list of tuples containing all possible two card combinations of deck, order doesnt matter"""
    ls = []
    for i in range(len(deck)-1):
        for j in range(i+1, len(deck)):
            ls.append((deck[i],deck[j]))
    return ls

d = Deck(True) #create a standard deck, cards faceUp so that we can see them when printing
d.shuffle()

#fp = open("testing/testing_handstrength_analysis.txt", "a") #write results into a file
fp = None 
#use fp = open(...) if I want to write to file

## round 1: preflop (no known cards except for pocket cards)
print("Preflop:", file = fp)
pocket = [d.pop(), d.pop()]
community = []
print(f"pocket cards = {pocket}", file=fp)
print(f"community = {community}", file=fp)

start = perf_counter()
h = handstrength(pocket, community)
end = perf_counter()
print(f"estimated hand strength = {h}", file=fp)
print(f"time = {end-start}s\n", file=fp)


## round 2: flop (3 known community cards)
# I will compare with doing the "true" hand strength (computed by trying all the different possibilities)
# to see if my estimated hand strength is representative
print("\nFlop:", file=fp)
community = [d.pop(), d.pop(), d.pop()]
print(f"pocket cards = {pocket}", file=fp)
print(f"community = {community}\n", file=fp)

#computing all combinations to get true hand strength:
start = perf_counter()
wins = 0 # i decide that wins include ties because don't lose any money
total = 0

for cards in pocketcombinations(d.deck): #find all combos for turn+river
    temp = d.deck.copy()
    temp.remove(cards[0])
    temp.remove(cards[1])
    rest = list(cards)
    for hand2 in pocketcombinations(temp): #for each of those combos, find all combos for opponent pocket cards
        result = getwinner(pocket+community+rest, list(hand2)+community+rest)
        if result != "Loss":
            wins +=1
        total+=1
P = wins/total
end = perf_counter()
print(f"total number of operations = {total}", file=fp)
print(f"true hand strength = {P}", file=fp)
print(f"time = {end-start}s\n", file=fp)

#using sampling: 10 * 1000 = 10 000 iterations
start = perf_counter()
h = handstrength(pocket, community)
end = perf_counter()
print(f"estimated hand strength = {h}", file=fp)
print(f"time = {end-start}s", file=fp)
print("Percent error = {:.3f}%\n".format((abs(h-P)/P)*100), file=fp)


## round 3: turn (4 known community cards, unkown river)
print("\nTurn:", file=fp)
community.append(d.pop())
print(f"pocket cards = {pocket}", file=fp)
print(f"community = {community}\n", file=fp)

#doing all combinations for true hand strength:
start = perf_counter()
wins = 0 # i decide that wins include ties because don't lose any money
total = 0

for card in d.deck: # first do all possible rivers
    temp = d.deck.copy()
    temp.remove(card)
    river = [card]
    for hand2 in pocketcombinations(temp):
        result = getwinner(pocket+community+river, list(hand2)+community+river)
        if result != "Loss":
            wins +=1
        total+=1
P = wins/total
end = perf_counter()
print(f"total number of operations = {total}", file=fp)
print(f"true hand strength = {P}", file=fp)
print(f"time = {end-start} s\n", file=fp)

# doing random sampling: 10*1000 = 10 000 iterations 
start = perf_counter()
h = handstrength(pocket, community)
end = perf_counter()
print(f"estimated hand strength = {h}", file=fp)
print(f"time = {end-start}s", file=fp)
print("Percent error = {:.3f}%\n".format((abs(h-P)/P)*100), file=fp)


## round 4: river (all community cards known)

print("\nRiver:", file=fp)
community.append(d.pop())
print(f"pocket cards = {pocket}", file=fp)
print(f"community = {community}\n", file=fp)

#doing all possible combinations: true hand strength
start = perf_counter()
wins = 0 
total = 0

for hand2 in pocketcombinations(d.deck): #get all possible combinations for opponents pocket cards
    result = getwinner(pocket+community, list(hand2)+community)
    if result != "Loss":
        wins +=1
    total+=1

P = wins/total
end = perf_counter()
print(f"total number of operations = {total}", file=fp)
print(f"true hand strength = {P}", file=fp)
print(f"time = {end-start} s\n", file=fp)

# doing random sampling: 10*1000 = 10 000 iterations 
start = perf_counter()
h = handstrength(pocket, community)
end = perf_counter()
print(f"estimated hand strength = {h}", file=fp)
print(f"time = {end-start}s", file=fp)
print("Percent error = {:.3f}%".format((abs(h-P)/P)*100), file=fp)

#fp.close()