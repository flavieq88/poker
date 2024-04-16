"""
Flavie Qin 2230509
Programming Techniques and Applications
R. Vincent, instructor
Final Project
"""

import os
import sys
sys.path[0] = sys.path[0].strip(r"\testing")

from winninghand import *
from random import shuffle

# testing the small functions

#testing flush
hand1 = [Card(12, "Heart"), Card(11, "Heart"), Card(10, "Heart"), Card(8, "Heart"), 
            Card(9, "Heart"), Card(14, "Heart"), Card(5, "Diamond")]
hand2 = [Card(12, "Heart"), Card(11, "Spade"), Card(2, "Diamond"), Card(8, "Heart"), 
            Card(6, "Club"), Card(14, "Heart"), Card(5, "Diamond")]
assert flush(hand1) == sorted([Card(8, "Heart"), Card(9, "Heart"), Card(10, "Heart"), 
                        Card(11, "Heart"), Card(12, "Heart"), Card(14, "Heart")], reverse=True)
assert not flush(hand2)

#testing straight
hand3 = [Card(13, "Heart"), Card(11, "Heart"), Card(10, "Heart"), Card(8, "Heart"), 
            Card(9, "Heart"), Card(14, "Heart"), Card(8, "Diamond")]
hand4 = [Card(6, "Heart"), Card(3, "Spade"), Card(2, "Diamond"), Card(4, "Heart"), 
            Card(13, "Club"), Card(14, "Heart"), Card(5, "Diamond")]
hand5 = [Card(6, "Heart"), Card(3, "Spade"), Card(2, "Diamond"), Card(4, "Heart"), 
            Card(13, "Club"), Card(14, "Heart"), Card(12, "Diamond")]
assert straight(hand1) == [Card(8, "Heart"), Card(9, "Heart"), Card(10, "Heart"), 
                            Card(11, "Heart"), Card(12, "Heart")]
assert not straight(hand2)
assert not straight(hand3) #checking if counter=5 but not a straight works
#checking if Ace 2 3 4 5 works and if longer sequences than 5 work
assert straight(hand4) == [Card(14, "Heart"), Card(2, "Diamond"), Card(3, "Spade"), 
                            Card(4, "Heart"), Card(5, "Diamond"), Card(6, "Heart")]
assert not straight(hand5) #check if 2 3 4 5 but no ace works 

#testing count_ranks:
d_hand1 = count_ranks(hand1)
assert list(d_hand1.keys()) == [14, 12, 11, 10, 9, 8, 5]
assert d_hand1[14] == [Card(14, "Heart")]

#testing four_kind
hand6 = [Card(6, "Heart"), Card(6, "Spade"), Card(6, "Diamond"), Card(4, "Heart"), 
            Card(6, "Club"), Card(3, "Heart"), Card(5, "Diamond")]
d_hand6 = count_ranks(hand6)
assert four_kind(d_hand6) == [Card(6, "Heart"), Card(6, "Spade"), Card(6, "Diamond"), 
                                Card(6, "Club"), Card(5, "Diamond")]
assert four_kind(d_hand1) == False

#testing three_kind
hand7 = [Card(6, "Heart"), Card(6, "Spade"), Card(14, "Diamond"), Card(4, "Heart"), 
            Card(6, "Club"), Card(3, "Heart"), Card(5, "Diamond")]
d_hand7 = count_ranks(hand7)
assert three_kind(d_hand7) == [Card(6, "Heart"), Card(6, "Spade"), Card(6, "Club"), 
                                Card(14, "Diamond"), Card(5, "Diamond")]
assert three_kind(d_hand1) == False

#testing two_pair
hand8 = [Card(6, "Heart"), Card(6, "Spade"), Card(14, "Diamond"), Card(14, "Heart"), 
            Card(2, "Club"), Card(5, "Heart"), Card(7, "Diamond")]
d_hand8 = count_ranks(hand8)
assert two_pairs(d_hand1) == False
assert two_pairs(d_hand8) == [Card(14, "Diamond"), Card(14, "Heart"), Card(6, "Heart"), 
                                Card(6, "Spade"), Card(7, "Diamond")]
#testing pair
hand9 = [Card(6, "Heart"), Card(6, "Spade"), Card(14, "Diamond"), Card(7, "Heart"), 
            Card(5, "Club"), Card(11, "Heart"), Card(2, "Diamond")]
d_hand9 = count_ranks(hand9)
assert pair(d_hand1) == False
assert pair(d_hand9) == [Card(6, "Heart"), Card(6, "Spade"), Card(14, "Diamond"), 
                            Card(11, "Heart"), Card(7, "Heart")]
#testing high_card
hand10 = [Card(12, "Heart"), Card(11, "Heart"), Card(10, "Heart"), Card(8, "Heart"), 
            Card(9, "Heart"), Card(14, "Heart"), Card(5, "Diamond")]
assert highcard(hand10) == [Card(14, "Heart"), Card(12, "Heart"), Card(11, "Heart"), 
                            Card(10, "Heart"), Card(9, "Heart")]


#testing rankHand:

a = [Card(12, "Heart"), Card(11, "Heart"), Card(10, "Heart"), Card(13, "Heart"), 
             Card(9, "Heart"), Card(14, "Heart"), Card(5, "Diamond")] # royal flush
b = [Card(12, "Heart"), Card(11, "Heart"), Card(10, "Heart"), Card(13, "Heart"), 
             Card(9, "Heart"), Card(2, "Heart"), Card(5, "Diamond")] # straight flush
c = [Card(12, "Heart"), Card(12, "Spade"), Card(12, "Diamond"), Card(13, "Heart"), 
             Card(12, "Club"), Card(2, "Heart"), Card(5, "Diamond")] # four of a kind
d = [Card(12, "Heart"), Card(12, "Spade"), Card(12, "Diamond"), Card(13, "Heart"), 
             Card(2, "Club"), Card(2, "Heart"), Card(5, "Diamond")] # full house
e = [Card(12, "Heart"), Card(11, "Spade"), Card(10, "Heart"), Card(13, "Heart"), 
             Card(9, "Heart"), Card(2, "Heart"), Card(5, "Diamond")] # flush
f = [Card(14, "Spade"), Card(2, "Spade"), Card(3, "Club"), Card(4, "Spade"), 
          Card(5, "Spade"), Card(11, "Club"), Card(3, "Diamond")] #straight A 2 3 4 5
g = [Card(12, "Heart"), Card(12, "Spade"), Card(12, "Diamond"), Card(13, "Heart"), 
             Card(2, "Club"), Card(7, "Heart"), Card(5, "Diamond")] # three of a kind
h =  [Card(12, "Heart"), Card(12, "Spade"), Card(2, "Diamond"), Card(13, "Heart"), 
             Card(2, "Club"), Card(7, "Heart"), Card(5, "Diamond")] # two pair
i = [Card(12, "Heart"), Card(12, "Spade"), Card(2, "Diamond"), Card(13, "Heart"), 
             Card(14, "Club"), Card(7, "Heart"), Card(5, "Diamond")] # one pair
j = [Card(4, "Heart"), Card(12, "Spade"), Card(2, "Diamond"), Card(13, "Heart"), 
             Card(14, "Club"), Card(7, "Heart"), Card(5, "Diamond")] # high card

assert rankHand(a)[0] == 9
assert rankHand(b)[0] == 8
assert rankHand(c)[0] == 7
assert rankHand(d)[0] == 6
assert rankHand(e)[0] == 5
assert rankHand(f)[0] == 4
assert rankHand(g)[0] == 3
assert rankHand(h)[0] == 2
assert rankHand(i)[0] == 1
assert rankHand(j)[0] == 0

g = [Card(4, "Heart"), Card(4, "Club"), Card(6, "Heart"), Card(9, "Club"), 
     Card(2, "Club"), Card(14, "Heart"), Card(3, "Spade")]
assert rankHand(g)[0]==1 #make sure it works if counter =4 but not high enough range due to repeats

# testing getwinner
assert a>b
assert f>h
assert getwinner(a, b) == "Win"
assert getwinner(h, f) == "Loss"
assert getwinner(c, c) == "Tie"
j_prime = [Card(4, "Spade"), Card(12, "Spade"), Card(2, "Diamond"), Card(13, "Heart"), 
             Card(14, "Club"), Card(7, "Heart"), Card(5, "Club")] # same as j but changing suits
assert getwinner(j, j_prime) == "Tie"

print("All tests passed")


STANDARDDECK = [Card(i,j, True) for j in ["Club", "Diamond", "Heart", "Spade"] 
                     for i in range(2, 15)]


# checking rankHand and getwinner are correct
n = 0
while n<100:
    shuffle(STANDARDDECK)
    community = STANDARDDECK[:5]
    hand1 = STANDARDDECK[5:7] + community
    hand2 = STANDARDDECK[7:9] + community
    print("hand1 =", hand1, rankHand(hand1))
    print("hand2 =", hand2, rankHand(hand2))
    print(getwinner(hand1, hand2))
    n +=1
# manually chekcing, all looks good