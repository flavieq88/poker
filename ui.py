#identification section
from players import *
from bot import *

import tkinter as tk            # for the GUI + event driven programming
import time

class PokerGame(tk.Tk): # base class is Tk
    """Application class for actually playing Poker"""

    #define stuff about the basic interface
    HEIGHT = 600 #how big the window will be
    WIDTH = 1000
    BACKGROUND = "#0b3b14" #make background dark green like real poker tables
    #for plaing all buttons and images, i define the table to be 3 rows and 7 columns

    #seperate the table into a grid pattern (just so its easier for me to place the stuff)
    ROWS = 6
    COLUMNS = 14

    #define some game states
    INPLAY = 1 # human player's turn
    GAMEOVER = 2 # game is over
    WAITING = 4 # human player is waiting


    def __init__(self, username = "", difficulty="EASY", SB = 5):
        """Initializes the application"""
        super().__init__(None) # initialize the base class

        self.username = username

        #other attributes for the game itself:
        self.players = [Player(), Bot(difficulty)]
        self.smallblind = SB # save value for the small blnid and big blinds
        self.SBplayer = 1    # initialize this attribute, will keep track of the index of self.players who is smallblind
                             # start with value 1 so that player ends up as first small blind
        self.lastraise = SB  # this will keep track of the amount the last raise was (for legal minimum of raising), min is SB if no one has raised yet

        # initialize stuff for starting the game
        self.state = self.WAITING
        

        self.draw_initial() # draw the table and labels and stuff
        self.title("POKER TIME")

        self.new_round() # start a new round
        

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
        self.potlabel.grid(row=0, column=1, sticky="s")
        self.humanlabel.grid(row = 4, column = 5, columnspan = 4, sticky="e")
        self.computerlabel.grid(row = 0, column = 8, sticky="e")
        # all the "sticky" attributes just deal with which way the label sticks to in the grid formation (just placement)

        #draw extra stuff: image of a stack of cards
        self.stackcards = tk.PhotoImage(file="images/stack.gif")
        cardlabel = tk.Label(image=self.stackcards)
        cardlabel.grid(row=2, column = 0, rowspan=2, columnspan=2)

        #also initialize the buttons to avoid errors
        self.checkbutton = tk.Button(self, text= "CHECK", command=self.on_click_check) #check button
        self.checkbutton.grid(row=4, column=3)
        self.callbutton = tk.Button(self, text=f"CALL", command=self.on_click_call) #call button
        self.callbutton.grid(row=4, column=2)
        self.raiseslider = tk.Scale(self, from_ =0, to=0) # slider for raising
        self.raisebutton = tk.Button(self, text = "RAISE", command=self.on_click_raise) # label for the raise slider 
        self.raiseslider.grid(row=4, column=1)
        self.raisebutton.grid(row=5, column=1) #position the label close enough
        self.foldbutton = tk.Button(self, text="FOLD", command=self.on_click_fold) #the fold button
        self.foldbutton.grid(row=4, column=4)
        
        #initilalize the SB BB labels too
        self.humanblind = tk.Label(self, text="SMALL BLIND" if self.SBplayer==0 else " BIG BLIND ")
        self.humanblind.grid(row=5, column=8, sticky="e")
        self.botblind = tk.Label(self, text="SMALL BLIND" if self.SBplayer==1 else " BIG BLIND ")
        self.botblind.grid(row=1, column=8, sticky="e")

        #initilize the pot amount labels
        self.potamount = tk.Label(self, text=f"0$")
        self.humanbalance = tk.Label(self, text = f"{self.players[0].balance}$")
        self.humanbet = tk.Label(self, text = f"Bet: {self.players[0].lastbet}$\nTotal bet: {self.players[0].totalbet}$")
        self.computerbalance = tk.Label(self, text=f"{self.players[1].balance}$")
        self.computerbet = tk.Label(self, text = f"Bet: {self.players[1].lastbet}$\nTotal bet: {self.players[1].totalbet}$")
        self.potamount.grid(row=1, column=1)
        self.humanbalance.grid(row = 4, column = 8, sticky="se")
        self.humanbet.grid(row = 4, column = 7, sticky = "s")
        self.computerbalance.grid(row = 1, column = 8, sticky="ne")
        self.computerbet.grid(row = 1, column = 7, sticky = "n")


    def blinds(self):
        """Makes each player post their blinds"""

        self.SBplayer = (self.SBplayer+1) % len(self.players)  #switch small blind and big blind, modulo for wrap around

        if self.players[self.SBplayer].balance < self.smallblind: #SB player doesnt have enough to pay up
            self.players[self.SBplayer].alive = False #player is dead
            self.game_over()
            return
        
        if self.players[(self.SBplayer+1)%2].balance <= 2*self.smallblind: #BB player does not have enough to pay up
            self.players[(self.SBplayer+1)%2].alive = False # player is dead
            self.game_over()
            return

        #update attriutes for pots and stuff
        self.players[self.SBplayer].balance -= self.smallblind #pay small blind
        self.players[self.SBplayer].totalbet += self.smallblind
        self.players[self.SBplayer].lastbet += self.smallblind
        self.players[self.SBplayer].did_action = True #kickstarted the preflop phase
        self.players[(self.SBplayer+1)%2].balance -= 2*self.smallblind #big blind = double the small blind
        self.players[(self.SBplayer+1)%2].totalbet += 2*self.smallblind
        self.players[(self.SBplayer+1)%2].lastbet += 2*self.smallblind
        self.players[(self.SBplayer+1)%2].did_action = True #kickstarted the preflop phase

        self.pot = 3*self.smallblind #add SB BB contributions

        self.update_pots() #display these changes

        #draw labels for small blind and big blind
        self.humanblind.config(text="SMALL BLIND" if self.SBplayer==0 else "BIG BLIND")
        self.botblind.config(text="SMALL BLIND" if self.SBplayer==1 else "BIG BLIND")

        if self.SBplayer == 1: # if computer is small blind, it should act first (since blinds are at preflop stage)
            self.computer_turn()


    def update_cards(self):
        """Displays all the updated the cards on the GUI
        Cards will be: either the actual card if face up
        Or the back if its supposed to be a hidden card
        Or green (colour of background) if no card has yet been placed 
        All of this is done "automatically" just by using the string of the item in the list when looking up the png
        """
        #first, display the cards in human players pocket cards
        for i in range(len(self.players[0].pocket)):
            path = f"images/{str(self.players[0].pocket[i])}.gif"
            self.cards[i][0] = tk.PhotoImage(file=path)
            self.cards[i][1] = tk.Label(image=self.cards[i][0])
            self.cards[i][1].grid(row=4, column = 10+2*i, rowspan=2, columnspan=2)

        #then display the community cards in middle
        for j in range(len(self.community)):
            path = f"images/{str(self.community[j])}.gif"
            self.cards[2+j][0] = tk.PhotoImage(file = path)
            self.cards[2+j][1] = tk.Label(image=self.cards[2+j][0])
            self.cards[2+j][1].grid(row=2, column = 4+2*j, rowspan=2, columnspan=2)

        #lastly display the pocket cards iof the oopponent (bot)
        for k in range(len(self.players[1].pocket)):
            path = f"images/{str(self.players[1].pocket[k])}.gif"
            self.cards[7+k][0] = tk.PhotoImage(file=path)
            self.cards[7+k][1] = tk.Label(image=self.cards[7+k][0])
            self.cards[7+k][1].grid(row=0, column = 10+2*k, rowspan=2, columnspan=2)
        
    
    def update_pots(self):
        """Updates the displayed values for the pot and each player balance pile and bets"""
        self.potamount.config(text=f"{self.pot}$")
        self.humanbalance.config(text = f"{self.players[0].balance}$")
        self.humanbet.config(text = f"Bet: {self.players[0].lastbet}$\nTotal bet: {self.players[0].totalbet}$")
        self.computerbalance.config(text=f"{self.players[1].balance}$")
        self.computerbet.config(text = f"Bet: {self.players[1].lastbet}$\nTotal bet: {self.players[1].totalbet}$")
        #now display the labels
        

    def legal_moves(self):
        """Returns a list of lists of the legl moves for both player
        the index of tuple will indicate the player index
        """
        n = len(self.players)
        legal = [[False, False, False, False] for _ in range(n)] 
        #each list will strore the legal moves for the player
        # order within each list: 
        # 0 = check (True or False if legal), 
        # 1 = call  (Amount it will call to),
        # 2 = raise (tuple (min, max) for raise to amount, 
        # 3 = fold (always legal)

        for i in range(n): #repeat for all players
            if self.players[i].balance == 0: #already went all in = cant do any moves anymore
                continue #will have False evreywhere and go to next player
            
            #handle check legality:
            if self.players[(i+1)%2].lastbet == 0: # check is available if other player hasnt bet money that phase yet
                legal[i][0] = True

            #handle call legality
            # call always legal but the value may change
            if self.players[(i+1)%2].totalbet > self.players[i].balance+self.players[i].totalbet: #if amount required to call is over the balance
                legal[i][1] = self.players[i].balance+self.players[i].lastbet #can only go all in if call
            elif self.players[(i+1)%2].lastbet == 0:
                #cannot call if opponent didnt bet anything
                legal[i][1] = False
            else:
                legal[i][1] = self.players[(i+1)%2].lastbet #match the other player's last bet
            
            #handle raise legality
            if self.players[(i+1)%2].balance == 0: #if oher person went all in, cannot raise
                legal[i][2] = False
            elif legal[i][1] == self.players[i].balance+self.players[i].lastbet: #if the call needed is already all in, no need for raise'
                legal[i][2] = False
            elif self.lastraise+self.players[(i+1)%2].lastbet >= self.players[i].balance:#if minimum raise needed is more than balance: only way is to do all in
                legal[i][2] = (self.players[i].balance+self.players[i].lastbet, self.players[i].balance+self.players[i].lastbet)
            elif self.players[i].balance != 0: #must have money left to raise
                legal[i][2] = (self.lastraise+self.players[(i+1)%2].lastbet, self.players[i].balance+self.players[i].lastbet) #max raise is to go all in
            
            #handle fold legality:
            legal[i][3] = True

        return legal


    def update_buttons(self):
        """Updates the buttons and draws them ONLY IF LEGAL so player has no choice but to do a legal move"""
        
        legal = self.legal_moves()[0] #only get legal moves for human player since buttons are for humans
        print("human =", legal)

        if legal[0]: #check is not False  
            self.checkbutton.grid(row=4, column=3)
        else:
            self.checkbutton.grid_remove() #make it disappear

        if legal[1]: #call is not False
            self.callbutton.config(text=f"CALL {legal[1]:4d}$") # modufy text in button for call 
            self.callbutton.grid(row=4, column=2)
        else:
            print("call not possible for human")
            self.callbutton.grid_remove() #make it disappear

        if legal[2]: #raise is not False
            self.raiseslider.config(from_ =legal[2][1], to=legal[2][0]) # slider for raising
            self.raiseslider.grid(row=4, column=1)
            self.raisebutton.grid(row=5, column=1) 
        else:
            self.raisebutton.grid_remove() #make it disappear
            self.raiseslider.grid_remove()

        if legal[3]: #fold is not False
            self.foldbutton.grid(row=4, column=4)
        else:
            self.foldbutton.grid_remove() #make it disappear


    def game_over(self):
        """Called when a game of poker is over"""
        if self.players[0].alive: #human is alive = they won
            self.title(f"{self.username} WINS")
        else:
            self.title(f"LEVEL {self.players[1].difficulty} BOT WINS")
        self.after(1000, self.quit()) #close the window after one second
        
    def give_pocket(self):
        """Distributes pocket cards"""
        for i in range(2): #2 cards per player
            self.players[0].pocket[i] = self.deck.pop(faceUp = True) 
            self.players[1].pocket[i] = self.deck.pop(faceUp = False) #not visible to us
        self.update_pots()
        self.update_cards()
        self.update_buttons()


    def give_cards(self):
        """Distributes some cards (determined by how many cards already in table)
        Marks a new phase"""
        def _number_of_None(ls):
            """Helper function that returns the number of None in a list of cards"""
            count = 0
            for card in ls:
                if str(card) == "None": #need to take strings becaseu Card class doesnt support comparison with Nonetype object
                    count+=1
            return count
        

        for i in range(len(self.players)):
            self.players[i].lastbet = 0 #reset the "last bet" of the phase to 0 since new phase
            self.players[i].did_action = False #means that the players havent yet done an action Yet this phase

        if _number_of_None(self.community) == 5: # no cards yet = at beginning
            for i in range(3):
                self.community[i] = self.deck.pop(faceUp = True)

        elif _number_of_None(self.community) == 2: # turn
            self.community[3] = self.deck.pop(faceUp=True)

        elif _number_of_None(self.community) == 1: #river
            self.community[4] = self.deck.pop(faceUp=True)
        
        elif _number_of_None(self.community) == 0: #no cards left but give cards was called = showdown
            self.state = self.WAITING
            self.update_buttons()
            self.showdown()
            return
        
        self.update_pots()
        self.update_cards()

        if self.SBplayer == 0 and (not all(self.legal_moves()[1])): #computer is bigblind = acts first postflop and also not in showdown
            self.computer_turn()
        
        self.update_buttons()

        self.state = self.INPLAY # now will be player turn to act
        

    
    def new_round(self):
        """Initializes stuff when a new round happens"""
        self.state = self.WAITING
        self.pot = 0 # reinitialize pot 
        self.community = [None for _ in range(5)] #list of 5 Nones to begin with
        self.deck = Deck() #make a new deck
        self.deck.shuffle() #shuffle the deck

        for i in range(len(self.players)): #reinitilize all stuff for each player
            self.players[i].inPlay = True
            self.players[i].did_action = False
            self.players[i].lastbet = 0
            self.players[i].totalbet = 0
            self.players[i].pocket = [None, None]

        self.cards = [[None, None] for _ in range(len(self.community) + 2*len(self.players))] # 9 total cards
         # i will use this to store the images and labels for the cards when displaying them 
        self.lastraise = self.smallblind

        self.update_cards()
        time.sleep(0.5)
        
        self.blinds() #make the players pay their blinds
        self.give_pocket() #give pocket cards
        time.sleep(0.5)

        self.state = self.INPLAY # now it is the turn for the player. 


    def end_round(self):
        """Distributes the pot to whoever won (in a case of no showdown)"""
        if self.players[0].inPlay:
            print("You won this round!")
            self.players[0].balance += self.pot
        else: #bot still in play = human lost
            print("You lost this round!")
            self.players[1].balance += self.pot
        self.update_pots()
        self.after(1000, self.new_round()) #wait 1000 ms before new round so you can see the changes

    def showdown(self):
        """Determines winner and redistributes pot in the case of a showdown"""
        self.state = self.WAITING
        self.update_buttons() #should be all cleared
        print("showdown")
        time.sleep(1)
        for i in range(len(self.players[1].pocket)):
            self.players[1].pocket[i].flip()
            print(self.players[1].pocket[i])
        self.update_cards()
        #display the rest of the cards one by one if not all shown yet
        for i in range(len(self.community)):
            if str(self.community[i]) == "None":
                self.community[i] = self.deck.pop(faceUp=True)
                time.sleep(1)
                self.update_cards #delay so adds suspense
                print("new card")
        humanresult = getwinner(self.players[0].pocket+self.community, self.players[1].pocket+self.community)
        if humanresult == "Win":
            #human won so main pot goes to human
            if 2*self.players[0].totalbet < self.pot: #but they can only get from opponent as much as they put in
                self.players[0].balance += 2*self.players[0].totalbet 
                self.players[1].balance += self.pot - 2*self.players[0].totalbet
            else: #generally they have equal total bets
                self.players[0].balance += self.pot
            print("YOU WON")
        elif humanresult == "Loss":
            #human lost so all the pot goes to bot
            if 2*self.players[1].totalbet < self.pot: #but they can only get from opponent as much as they put in
                self.players[1].balance += 2*self.players[1].totalbet 
                self.players[0].balance += self.pot - 2*self.players[1].totalbet
            else: #generally they have equal total bets
                self.players[1].balance += self.pot
            print("YOU LOST")
        else: #its a tie
            #each player just gets back the total bets they gave
            self.players[0].balance += self.players[0].totalbet
            self.players[1].balance += self.players[1].totalbet
            print("ITS A TIE")

        self.new_round()
        

    def computer_turn(self):
        """Makes the game sleep for a second then let computer make an action"""
        if self.state == self.INPLAY:
            return #should be the players turn so ignore
        time.sleep(1)
        x = self.players[1].doAction(self.community, self.players[0], self.pot, self.legal_moves()[1])
        if x != None: # return a value = did raise
            self.lastraise = x
            print(self.lastraise)
        self.pot = self.players[0].totalbet + self.players[1].totalbet
        self.update_pots()
        self.update_buttons()

        if not self.players[1].inPlay: #if bot folded
            self.end_round()
            return
        
        if self.if_agree(): #can move on
            if self.players[0].balance==0 or self.players[1].balance==0:
                self.showdown()
                return
            else:
                self.give_cards()
        else: # if not, time for human turn, cannot proceed
            self.state = self.INPLAY



    def on_click_fold(self):
        """Defines what happens on a click for the FOLD button"""
        if self.state != self.INPLAY:
            return #ignore button clicks when it is not player turn
        self.players[0].fold()
        self.state = self.WAITING
        self.end_round()


    def on_click_raise(self): 
        """Defines what happens on a click for the RAISE button"""
        if self.state != self.INPLAY:
            return #ignore button clicks when it is not player turn
        amount = self.raiseslider.get()
        self.lastraise = self.players[0].raisebet(self.players[1], amount)
        print(self.lastraise)
        self.pot = self.players[0].totalbet + self.players[1].totalbet
        self.after_action()

    
    def on_click_call(self):
        if self.state != self.INPLAY:
            return #ignore button clicks when it is not player turn
        call_amount=self.legal_moves()[0][1]
        self.players[0].callbet(call_amount)
        self.pot = self.players[0].totalbet + self.players[1].totalbet
        self.after_action()
    
    def on_click_check(self):
        if self.state != self.INPLAY:
            return #ignore button clicks when it is not player turn
        #if pressed check
        self.players[0].check()
        self.after_action()
        
    
    def after_action(self):
        """Does the stuff after a player does an action"""
        self.state = self.WAITING
        self.update_pots()
        print("checking actions")

        if self.if_agree() and (self.players[0].balance == 0 or self.players[1].balance == 0):
            self.showdown()
            return
        
        if not self.if_agree():
            self.computer_turn()
        else: # agree = can move on
            self.give_cards()

    def if_agree(self):
        """Returns True if the betting round ends because they agree"""
        #case 1: they have same total bet:
        print("human="+str(self.players[0].totalbet), self.players[0].did_action)
        print("bot="+str(self.players[1].totalbet), self.players[1].did_action)
        if not (self.players[0].did_action and self.players[1].did_action):
            print("doesnt match)")
            return False #if not both did an action in a phase, then didnt agree yet
            
        if self.players[0].totalbet == self.players[1].totalbet:
            print("matching bet")
            return True # no need to worry about beginning of round since blinds means no time will have same total bet unless agree!
        #case 2: they dont have same total bet, but one went all in and other has called higher already
        if self.players[0].balance == 0 and self.players[1].totalbet >= self.players[0].totalbet:
            # this means human went all in and bot agreed (either matched it or has already bet more)
            return True
        if self.players[1].balance == 0 and self.players[0].totalbet >= self.players[1].totalbet:
            # this means bot went all in and human agreed
            return True
        print("doesnt match")
        return False #any other cases no


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
        self.clicked.set("EASY")
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