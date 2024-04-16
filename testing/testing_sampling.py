"""
Flavie Qin 2230509
Programming Techniques and Applications
R. Vincent, instructor
Final Project
"""

import os
import sys
sys.path.append(os.getcwd())

from winninghand import *
from random import shuffle
from time import perf_counter

# to test if the sampling idea for hand strength is a repressentative measure of "real" hand strength

def pocketcombinations(deck):
    """Returns a list of tuples containing all possible pocket hands of deck, order doesnt matter"""
    ls = []
    for i in range(len(deck)-1):
        for j in range(i+1, len(deck)):
            ls.append((deck[i],deck[j]))
    return ls

deck = [Card(i,j, True) for j in ["Club", "Diamond", "Heart", "Spade"] 
                     for i in range(2, 15)]

shuffle(deck)
community = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]
hand1 = [deck.pop(), deck.pop()]
print(hand1)
print(community)

start = perf_counter()
wins = 0 # wins include ties because don't lose any money
total = 0
for hand2 in pocketcombinations(deck):
    result = getwinner(hand1+community, list(hand2)+community)
    if result != "Loss":
        wins +=1
    total+=1
print(wins, total)
P = wins/total
end = perf_counter()
print("True =", P)
print("Time = ", end-start)


#random sampling:

avg = 0
for i in range(50): #reapeat 10 times to get an idea
    start = perf_counter()
    wins = 0 # wins include ties because don't lose any money
    total = 0
    for i in range(1000): # number of iterations = size of random sample
        shuffle(deck)
        hand2 = deck[:2]
        result = getwinner(hand1+community, hand2+community)
        if result != "Loss":
            wins +=1
        total+=1
    print(wins, total)
    end = perf_counter()
    print("Sampling =", wins/total)
    print("time =", end-start)
    avg += wins/total
print("True =", P)
print("Avg =", avg/50)

"""
deck = [Card(i,j, True) for j in ["Club", "Diamond", "Heart", "Spade"] 
                     for i in range(2, 15)]

shuffle(deck)
community = [deck.pop(), deck.pop(), deck.pop(), deck.pop()]
hand1 = [deck.pop(), deck.pop()]
print(hand1)
print(community)


start = perf_counter()
wins = 0 # wins include ties because don't lose any money
total = 0
print(len(list(permutations(deck, 3))))
for combo in permutations(deck, 3):
    combo = list(combo)
    community += combo[:1]
    hand2 = combo[1:]
    result = getwinner(hand1+community, list(hand2)+community)
    if result != "Loss":
        wins +=1
    total+=1
    (print(total))
print(wins, total)
P = wins/total
end = perf_counter()
print("True =", P)
print("Time = ", end-start)
#other case: two community card missing, and opponents hands
#use permutations because order (which one in comunity and which one in pocket) actaulyl matters

#sampling method:
avg = 0
for i in range(10): #reapeat 10 times to get an idea
    start = perf_counter()
    wins = 0 # wins include ties because don't lose any money
    total = 0
    for i in range(1000): # number of iterations = size of random sample
        shuffle(deck)
        rest = deck[:3]
        temp = community + rest[:1]
        hand2 = rest[1:]
        result = getwinner(hand1+temp, hand2+temp)
        if result != "Loss":
            wins +=1
        total+=1
    print(wins, total)
    end = perf_counter()
    print("Sampling =", wins/total)
    print("time =", end-start)
    avg += wins/total
print("Avg =", avg/10)
"""