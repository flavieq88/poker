# Poker
I made a program so that you can play no limit Heads up Texas Hold'em poker (the user against a computer bot), in Python. 
This includes a Graphical User Interface.

![image](https://github.com/flavieq88/poker/assets/166056837/e2fb3260-1384-44fd-9eb9-e966a97f0987)

## Documentation
Then entire project was built in Python. Only standard Python libraries were used.

I used tkinter for the GUI and event driven programming.
 

## How to play
My application follows the standard rules for no limit Heads up Texas hold'em poker (including for blinds, betting rounds and hand rankings). 

To start playing, run the ui.py file.

## Computer bot and playing strategies
I implemented heuristics (rule based) computer bots to play poker against. 
It has 3 difficulty levels: easy, medium, hard.

The easy level bot just plays a random move, but if it chooses to fold while check is available, it will check instead.
<br>
For the medium and hard level bots, both calculate (a modified version of) pot odds and the handstrength of their own cards. 
<br>
The medium bot uses a more passive loose strategy (raise only if cards very good, and in preflop play pocket cards even if they are not very good).
The hard bot uses a more agressive tight strategy (raise even if cards are not very good, and in preflop play pocket cards only if they are very good).

