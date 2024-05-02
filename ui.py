#identification section
from players import *
from bot import *

import tkinter as tk            # for the GUI + event driven programming
from PIL import Image, ImageTk  # for displyaing images (cards)
import time                     # for sleep()

class PokerGame(tk.Tk): # base class is Tk
    """Application class for actually playing Poker"""

    #define stuff about the basic interface
    HEIGHT = 640 #how big the window will be
    WIDTH = 1000
    BACKGROUND = "#0b3b14" #make background dark green like real poker tables
    #for plaing all buttons and images, i define the table to be 3 rows and 7 columns

    #seperate the table into a grid pattern (just so its easier for me to place the stuff)
    ROWS = 6
    COLUMNS = 14

    #define some game states
    INPLAY = 1 # human player's turn
    GAMEOVER = 2 # game is over
    WAITING = 4 # players are waiting (both players agreed, no more betting)
    ENDROUND = 5 # at the end determine winner and give pot to winner and reinitialize stuff


    def __init__(self, username = "", SB = 5):
        """Initializes the application"""
        super().__init__(None) # initialize the base class

        self.username = username

        #other attributes for the game itself:
        self.players = [Player(), Bot(difficulty)]
        self.smallblind = SB # save value for the small blnid and big blinds
        self.SBplayer = 0   #initialize this attribute, will keep track of the index of self.players who is smallblind
                            #start with value 1 so that player ends up as first small blind

        # initialize stuff for starting the game
        self.state = self.WAITING
        self.new_round() # start a new round

        self.draw_initial() # draw the table and labels and stuff
        self.title("POKER TIME")
        
        self.update_buttons()
        self.update_cards()
        self.update_pots()

        

    
            
                


    def draw_initial(self):
        """Initializes the table and draws all the basic stuff
        All the stuff drawn here shouldnt need to be updated every (so only call this function once)
        But I separated into a function just so it was clearer in the init what i was doing"""
        # Create the window
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}") #make the default size of the window
        self.configure(background=self.BACKGROUND) # make the background color what we chose
    
        # make the rows and columns fill up all space
        for i in range(self.COLUMNS):
            self.grid_columnconfigure(i, weight = 1) #must add weight parameter so that stuff doesnt get smushed
        for i in range(self.ROWS):
            self.grid_rowconfigure(i, weight = 1)

        
        #makes labels labels and players names
        self.potlabel = tk.Label(self, text = "CURRENT POT AMOUNT:") #label the pot
        self.humanlabel = tk.Label(self, text=self.username)
        self.computerlabel = tk.Label(self, text=f"PLAYER2: LEVEL {self.players[1].difficulty}")

        #now display the labels
        self.potlabel.grid(row=2, column=1, sticky="n")
        self.humanlabel.grid(row = 4, column = 5, columnspan = 4, sticky="e")
        self.computerlabel.grid(row = 0, column = 8, sticky="e")
        # all the "sticky" attributes just deal with which way the label sticks to in the grid formation (just placement)


    def update_cards(self):
        """Displays all the updated the cards on the GUI
        Cards will be: either the actual card if face up
        Or the back if its supposed to be a hidden card
        Or green (colour of background) if no card has yet been placed 
        All of this is done "automatically" just by using the string of the item in the list when looking up the png
        """
        #first, display the cards in human players pocket cards
        for i in range(len(self.players[0].pocket)):
            path = f"images/{str(self.players[0].pocket[i])}.png"
            self.cards[i] = ImageTk.PhotoImage(Image.open(path))
            cardlabel = tk.Label(image=self.cards[i])
            cardlabel.grid(row=4, column = 10+2*i, rowspan=2, columnspan=2)

        #then display the community cards in middle
        for j in range(len(self.community)):
            path = f"images/{str(self.community[j])}.png"
            self.cards[2+j] = ImageTk.PhotoImage(Image.open(path))
            cardlabel = tk.Label(image=self.cards[2+j])
            cardlabel.grid(row=2, column = 4+2*j, rowspan=2, columnspan=2)

        #lastly display the pocket cards iof the oopponent (bot)
        for k in range(len(self.players[1].pocket)):
            path = f"images/{str(self.players[1].pocket[k])}.png"
            self.cards[7+k] = ImageTk.PhotoImage(Image.open(path))
            cardlabel = tk.Label(image=self.cards[7+k])
            cardlabel.grid(row=0, column = 10+2*k, rowspan=2, columnspan=2)

    
    def update_pots(self):
        """Updates the values for the pot and each player balance pile"""
        self.potamount = tk.Label(self, text=str(self.pot)+"$")
        self.humanbalance = tk.Label(self, text = str(self.players[0].balance)+"$")
        self.humanbet = tk.Label(self, text = f"Bet: {self.players[0].lastbet}$")
        self.computerbalance = tk.Label(self, text=str(self.players[1].balance)+"$")
        self.computerbet = tk.Label(self, text = f"Bet: {self.players[1].lastbet}$")
        #now display the labels
        self.potamount.grid(row=2, column=1)
        self.humanbalance.grid(row = 5, column = 8, sticky="ne")
        self.humanbet.grid(row = 5, column = 6, sticky = "n")
        self.computerbalance.grid(row = 1, column = 8, sticky="ne")
        self.computerbet.grid(row = 1, column = 6, sticky = "n")

    def update_buttons(self):
        """Updates the buttons and draws them"""
        # create and draw all the buttons
        self.foldbutton = tk.Button(self, text="FOLD", command=self.on_click) #the fold button
        self.checkbutton = tk.Button(self, text= "CHECK") # the check button
        self.callbutton = tk.Button(self, text="CALL") # button for raising
        self.raiseslider = tk.Scale(self, from_ =500, to=0) # slider for raising
        self.raisebutton = tk.Button(self, text = "RAISE") # label for the raise slider
        
        #now draw out the buttons
        self.foldbutton.grid(row=4, column=4) # draw it out. uses grid instead o fpack or place so that it doesnt look funky in full screen
        self.checkbutton.grid(row=4, column=3)
        self.callbutton.grid(row=4, column=2)
        self.raiseslider.grid(row=4, column=1)
        self.raisebutton.grid(row=5, column=1) #position the label close enough

    def game_over(self):
        """Called when a game of poker is over"""
        self.after(1000)
        print("here")
        pass
        if self.players[0].alive: #huamn is alive = they won
            self.title(f"{self.username} WINS")
        else:
            self.title(f"LEVEL {self.players[1].difficulty} BOT WINS")
        self.destroy() #close the window
    
    def give_cards(self):
        """Distributes some cards (determined by how many cards already in table)
        This function would only be called when game state is WAITING"""
        def _number_of_None(ls):
            """Helper function that returns the number of None in a list of cards"""
            count = 0
            for card in ls:
                if str(card) == "None": #need to take strings becaseu Card class doesnt support comparison with Nonetype object
                    count+=1
            return count
        
        if _number_of_None(self.players[0].pocket) == 2: # empty pocket ahnds so distribute pocket cards
            for i in range(2): #2 cards per player
                self.players[0].pocket[i] = self.deck.pop(faceUp = True) 
                self.players[1].pocket[i] = self.deck.pop(faceUp = False)
        elif _number_of_None(self.community) == 5: # no cards yet = at beginning
            for i in range(3):
                self.community[i] = self.deck.pop(faceUp = True)
        elif _number_of_None(self.community) == 2: # turn
            self.community[4] = self.deck.pop(faceUp=True)
        else: #river
            self.community[4] = self.deck.pop(faceUp=True)
        self.update_cards()

    
    def new_round(self):
        """Initializes stuff when a new round happens"""
        self.pot = 0 # reinitialize pot 
        self.community = [None for _ in range(5)] #list of 5 Nones to begin with
        self.deck = Deck() #make a new deck
        self.deck.shuffle() #shuffle the deck
        self.cards = [None for _ in range(len(self.community) + 2*len(self.players))] # 9 total cards
         # i will use this to store the images for the cards when displaying them 
        self.give_cards()
        self.SBplayer = (self.SBplayer+1) % len(self.players)  #switch small blind and big blind, modulo for wrap around

        if self.SBplayer == 1: # if computer is small blind, it should act first
            self.computer_turn()
        
        self.state = self.INPLAY # now it is the turn for the player. 
    


    def computer_turn(self):
        """Makes the game sleep for a second then let computer make an action"""
        self.after(1000, self.players[1].doAction(self))
        self.update_pots()



    def on_click(self):
        """Defines what happens on a click"""
        if self.state == self.GAMEOVER or self.state == self.WAITING:
            return #ignore button clicks when it is not player turn
        print("jere")
        
        



class Menu(tk.Tk):   
    """A class to display the inital menu"""
    def __init__(self):
        super().__init__(None) # initialize the base class
        self.value = "" # a place to store the response
        self.difficulty = "" # a place to store the difficulty level, either EASY, MEDIUM, HARD
        
        # draw the window
        self.canvas = tk.Canvas(self,
                                     width = 200,
                                     height = 30)
        self.canvas.pack()
        self.title = "Menu" #create window
        self.label0 = tk.Label(self, text="Choose your difficulty level")
        self.label0.pack()
        self.clicked = tk.StringVar() #set the dropdown menu options to be str
        options = ["EASY", "MEDIUM", "HARD"]
        self.clicked.set("HARD")
        self.menu = tk.OptionMenu(self, self.clicked, *options)
        self.menu.pack()
        self.label = tk.Label(self, text="Enter your username:\n(press enter to submit)")
        self.label.pack() #display label
        self.box = tk.Entry(self, validate="key", validatecommand=(self.register(self.validate_entry), "%P")) 
        # all the extra arguments for making the limit of text character to what i set
        self.box.pack(pady=20) #display the entry field
        
        self.bind("<Return>", lambda event=None: self.get_name()) #key bind return to function

    def get_name(self):
        self.difficulty = self.clicked.get()
        self.value = self.box.get().upper()
        self.destroy() #close the window

    def validate_entry(self, text):
        """Makes sure that the user inputs a string of less than 20 characters"""
        return len(text)<=25

    def return_stuff(self):
        """Returns a tuple of the username and difficulty level"""
        if self.value: #not empty
            return self.value, self.difficulty
        else: #if nothing submitted
            return "PLAYER1", self.difficulty



if __name__ == '__main__':
    menu = Menu() #first display the menu
    menu.mainloop()
    username, difficulty = menu.return_stuff() #get the info from menu
    app = PokerGame(username, difficulty) 
    app.mainloop() # start the game