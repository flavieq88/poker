#identification section
from players import *
from bot import *
import tkinter as tk
from PIL import Image, ImageTk

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
    WAITING = 3 # any other time (distributing cards or computer playing)

    def __init__(self, username = "", difficulty="HARD", SB = 5):
        """Initializes the application"""
        super().__init__(None) # initialize the base class

        #first: an opening menu to ask for username and bot difficulty
        #self.username, difficulty= self.menu()
        self.username = username
        self.difficulty = difficulty

        #other attributes for the game:
        self.players = [Player(), Bot(self.difficulty)]
        self.pot = 0
        self.smallblind = SB
        self.community = [None for _ in range(5)] #list of 5 None
        self.deck = Deck()

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
        self.foldbutton.grid(row=4, column=4, sticky="S") # draw it out. uses grid instead o fpack or place so that it doesnt look funky in full screen
        self.checkbutton.grid(row=4, column=3, sticky="S")
        self.callbutton.grid(row=4, column=2, sticky="S")
        self.raiseslider.grid(row=4, column=1, sticky="S")
        self.raisebutton.grid(row=5, column=1, sticky="N", pady = 10) #position the label close enough
        
        #makes labels labels and players names
        self.potlabel = tk.Label(self, text = "CURRENT POT AMOUNT:") #label the pot
        self.humanlabel = tk.Label(self, text=self.username)
        self.computerlabel = tk.Label(self, text=f"PLAYER2: LEVEL {self.difficulty}")
        #now display the labels
        self.potlabel.grid(row=2, column=1, sticky="n")
        self.humanlabel.grid(row = 4, column = 5, columnspan = 5, sticky="e", padx=15)
        self.computerlabel.grid(row = 0, column = 8, sticky="e")
        

        self.title("POKER TIME")
        self.update_cards()
        self.update_pots()


    
    def update_cards(self):
        """Displays all the updated the cards on the GUI
        Cards will be: either the actual card if face up
        Or the back if its supposed to be a hidden card
        Or white if no card has yet been placed 
        """
        #first, display the cards in human players pocket cards
        for i in range(len(self.players[0].pocket)):
            path = f"images/{str(self.players[0].pocket[i])}.png"
            self.image = ImageTk.PhotoImage(Image.open(path))
            label = tk.Label(image=self.image)
            label.grid(row=4, column = 10+2*i, rowspan=2, columnspan=2)

        #then display the community cards in middle
        for j in range(len(self.community)):
            path = f"images/{str(self.community[j])}.png"
            self.image = ImageTk.PhotoImage(Image.open(path))
            label = tk.Label(image=self.image)
            label.grid(row=2, column = 4+2*j, rowspan=2, columnspan=2)

        #lastly display the pocket cards iof the oopponent (bot)
        for k in range(len(self.players[1].pocket)):
            path = f"images/{str(self.players[1].pocket[k])}.png"
            self.image = ImageTk.PhotoImage(Image.open(path))
            label = tk.Label(image=self.image)
            label.grid(row=0, column = 10+2*k, rowspan=2, columnspan=2)
    
    def update_pots(self):
        """Updates the values for the pot and each player money pile"""
        self.potamount = tk.Label(self, text=str(self.pot)+"$")
        self.humanmoney = tk.Label(self, text = str(self.players[0].money)+"$")
        self.computermoney = tk.Label(self, text=str(self.players[1].money)+"$")
        #now display the labels
        self.potamount.grid(row=2, column=1)
        self.humanmoney.grid(row = 5, column = 8, sticky="ne")
        self.computermoney.grid(row = 1, column = 8, sticky="ne")


class Menu(tk.Tk):   
    def __init__(self):
        super().__init__(None) # initialize the base class
        self.value = "" # a place to store the response
        self.difficulty = "" # a place to store the difficulty level
        
        # draw the window
        self.canvas = tk.Canvas(self,
                                     width = 200,
                                     height = 40)
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
    menu = Menu()
    menu.mainloop()
    username, difficulty = menu.return_stuff()
    app = PokerGame(username, difficulty)
    app.mainloop()