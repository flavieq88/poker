#!/bin/python3
#run this file to play
#this file also includes start and end menus 

import tkinter as tk            # for the GUI + event driven programming
from game import PokerGame      # actual game engine

class StartMenu(tk.Tk):   
    """A class to display the inital menu"""
    def __init__(self):
        super().__init__(None) # initialize the base class
        self.value = "" # a place to store the response
        self.difficulty = "" # a place to store the difficulty level, either EASY, MEDIUM, HARD
        
        # draw the window
        self.canvas = tk.Canvas(self,
                                     width = 250,
                                     height = 30)
        self.canvas.pack()
        self.title = "Start Menu" #create window
        self.label0 = tk.Label(self, text="Choose your difficulty level:")
        self.label0.pack()
        self.clicked = tk.StringVar() #set the dropdown menu options to be str
        options = ["EASY", "MEDIUM", "HARD"]
        self.clicked.set("EASY")
        self.menu = tk.OptionMenu(self, self.clicked, *options)
        self.menu.pack()
        self.label = tk.Label(self, text="\nEnter your username:\n(press enter to submit)")
        self.label.pack() #display label
        self.box = tk.Entry(self, validate="key", validatecommand=(self.register(self.validate_entry), "%P")) 
        # all the extra arguments for making the limit of text character to what i set
        self.box.pack(pady=20) #display the entry field
        
        self.protocol("WM_DELETE_WINDOW", self.get_name) #make it so that if user closes the window, same as entering
        self.bind("<Return>", lambda event=None: self.get_name()) #key bind return to function

    def get_name(self):
        """Save the difficulty and name that the user inputted"""
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
        else: #if nothing submitted then give a default name
            return "PLAYER1", self.difficulty

class EndMenu(tk.Tk):   
    """A class to display the inital menu"""
    def __init__(self):
        super().__init__(None) # initialize the base class
        self.quitting = False #place to store the player response
        
        # draw the window
        self.canvas = tk.Canvas(self,
                                     width = 200,
                                     height = 30)
        self.canvas.pack()
        self.title = "End Menu" #create window
        self.label0 = tk.Label(self, text="Game over.\nWhat would you like to do?")
        self.label0.pack()
        self.quitbutton = tk.Button(self, text = "QUIT PLAYING", command = self.on_click_quit)
        self.quitbutton.pack(pady = 10)
        self.replaybutton = tk.Button(self, text = "PLAY AGAIN", command = self.on_click_replay)
        self.replaybutton.pack(pady= 10)

        self.protocol("WM_DELETE_WINDOW", self.on_click_quit) #make it so that if user closes the window, same as quitting

    def on_click_quit(self):
        """Handles the stuff when user decides to quit and stop playing"""
        self.quitting = True
        self.destroy()

    def on_click_replay(self):
        """Handles the stuff when user decides to play another game"""
        self.quitting = False
        self.destroy()


if __name__ == '__main__': #main code!!
    while True:
        startmenu = StartMenu() #first display the menu
        startmenu.mainloop()
        username, difficulty = startmenu.return_stuff() #get the info from menu
        app = PokerGame(username, difficulty) 
        app.mainloop() # start the game
        endmenu = EndMenu() #this onyl runs one the first game mainloop is over
        endmenu.mainloop()
        if endmenu.quitting == True: #only stop this loop if user decided to quit
            break

