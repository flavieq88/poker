#identification section
from players import *
from bot import *
import tkinter as tk
import PIL 

class PokerGame(tk.Tk): # base class is Tk
    """Application class for actually playing Poker"""

    #define stuff about the basic interface
    HEIGHT = 640 #how big the window will be
    WIDTH = 1000
    BACKGROUND = "#194f18" #make background dark green like real poker tables
    #for plaing all buttons and images, i define the table to be 3 rows and 7 columns

    #seperate the table into a grid pattern (just so its easier for me to place the stuff)
    ROWS = 6
    COLUMNS = 14

    #define some game states
    INPLAY = 1 # human player's turn
    GAMEOVER = 2 # game is over
    WAITING = 3 # any other time (distributing cards or computer playing)

    def __init__(self, SB = 5):
        """Initializes the application"""
        super().__init__(None) # initialize the base class

        #other attributes for the game:
        self.players = [Player(), Bot()]
        self.pot = 0
        self.smallblind = SB
        self.community = [None, None, None, None, None]

        # Create the window
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.configure(background=self.BACKGROUND)
    
        # make the rows and columns fill up all space
        for i in range(self.COLUMNS):
            self.grid_columnconfigure(i, weight=1)
        for i in range(self.ROWS):
            self.grid_rowconfigure(i, weight=1)
        

        # create and draw all the buttons
        self.foldbutton = tk.Button(self, text="FOLD") #the fold button
        self.checkbutton = tk.Button(self, text= "CHECK") # the check button
        self.callbutton = tk.Button(self, text="CALL") # button for raising
        self.raiseslider = tk.Scale(self, from_ =500, to=0) # slider for raising
        self.raisebutton = tk.Button(self, text = "RAISE") # label for the raise slider
        
        #now draw out the buttons
        self.foldbutton.grid(row=4, column=5, sticky="S") # draw it out. uses grid instead o fpack or place so that it doesnt look funky in full screen
        self.checkbutton.grid(row=4, column=4, sticky="S")
        self.callbutton.grid(row=4, column=3, sticky="S")
        self.raiseslider.grid(row=4, column=2, sticky="S")
        self.raisebutton.grid(row=5, column=2, sticky="N", pady = 10) #position the label close enough

        #now draw all the spaces for the cards: empty rectangles
        

        self.title("Play Poker! Gambling is fun :)")

if __name__ == '__main__':
    app = PokerGame()
    app.mainloop()