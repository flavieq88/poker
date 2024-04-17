"""
Flavie Qin 2230509
Programming Techniques and Applications
R. Vincent, instructor
Final Project
"""

import sys
sys.path[0] = sys.path[0].strip(r"\testing")

from winninghand import *
from bot import handstrength

from random import shuffle
from time import perf_counter

# to test if the sampling idea for hand strength is a representative measure of "real" hand strength
# also testing if theres a difference between averaging many small samples or one big sample
# saves this data into text file "testing_sampling_analysis.txt"


#helper function for finding true handstrength
def pocketcombinations(deck):
    """Returns a list of tuples containing all possible pocket hands of deck, order doesnt matter"""
    ls = []
    for i in range(len(deck)-1):
        for j in range(i+1, len(deck)):
            ls.append((deck[i],deck[j]))
    return ls

deck = [Card(i,j, True) for j in ["Club", "Diamond", "Heart", "Spade"] 
                     for i in range(2, 15)] #create a standard deck
fp = open("testing/testing_sampling_analysis.txt", "a") #write results into a file

shuffle(deck)
community = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
hand1 = [deck.pop(), deck.pop()]
print("hand1 =", hand1, file=fp)
print("community pile =", community, file=fp)
print("Finding hand strength of hand1 (probability it wins)\n", file = fp)

# first task: finding true handstrength
print("Doing all combinations:", file = fp)
start = perf_counter()
wins = 0 # i decide that wins include ties because don't lose any money
total = 0

for hand2 in pocketcombinations(deck):
    result = getwinner(hand1+community, list(hand2)+community)
    if result != "Loss":
        wins +=1
    total+=1

P = wins/total
end = perf_counter()
print("Number of operations =", total, file=fp)
print("True hand strength =", P, file=fp)
print("Time = ", end-start, "\n", file=fp)


# task 2: random sampling 1 sample of 1000 combinations
# task 3: random sampling 10 sample of 100 combinations (averaging)
tasks = [(1000, 1), (100, 10)] # (n_inter:n_samples)
for n_iter, n_samples in tasks:
    print(f"Sampling random combinations {n_samples} times:", file=fp)
    print(f"Number of iterations = {n_iter}",file=fp)
    start = perf_counter()
    h = handstrength(hand1, community, n_iter, n_samples)
    """
    for i in range(n_samples): #repeat 10 times to get an idea
        wins = 0 # wins include ties because don't lose any money
        total = 0
        for i in range(n_iter): # number of iterations = size of random sample
            shuffle(deck)
            hand2 = deck[:2]
            result = getwinner(hand1+community, hand2+community)
            if result != "Loss":
                wins +=1
            total+=1
        print("Sampling probability =", wins/total, file=fp)
        print("Percent error = {:3.2f}%".format(abs((wins/total-P)/P)*100), file=fp)
        print("Time =", end-start,, file=fp)
        avg += wins/total
    """
    end = perf_counter()
    print("Average sampling probability =", h, file = fp)
    print("Percent error over {} samples = {:3.2f}%\n".format(n_samples, abs(h-P)/P*100), file = fp)

fp.close()