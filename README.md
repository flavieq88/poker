# Poker
Poker program implemented from scratch, where you can play no limit Heads up Texas Hold'em poker against a computer bot. 

![image](https://github.com/flavieq88/poker/assets/166056837/e2fb3260-1384-44fd-9eb9-e966a97f0987)

## Documentation and setup
The entire project was built in Python. Only standard Python libraries were used so no installation required.
It includes a graphical user interface built with tkinter.
 
My application follows the standard rules for no limit Heads up Texas hold'em poker (including for blinds, betting and hand rankings). 

To start playing, run the ui.py file.

## Computer bot and playing strategies
I implemented heuristics (rule based) computer bots to play poker against. 
It has 3 difficulty levels: easy, medium, hard.

The easy level bot just plays a random move, but if it chooses to fold while check is available, it will check instead.

For the medium and hard level bots, both calculate (a modified version of) pot odds and the handstrength of their own cards. The hand strength is calculated using a random sampling method.

The medium bot uses a more passive loose strategy (raise only if cards very good, and in preflop play pocket cards even if they are not very good).

The hard bot uses a more aggressive tight strategy (raise even if cards are not very good, and in preflop play pocket cards only if they are very good).

