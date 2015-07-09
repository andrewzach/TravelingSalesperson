# Author:     Andrew Zacharias
# Student #:  D14127051
# Date:       May 2015

import tkinter
from tkinter import ttk
from guiframes import FlightCostFrame, CheapestRouteFrame, FileRouteFrame, SearchFrame
from traveldb import TravelDB
from travelcalc import TravelAgent
from inputoutput import InputHandler

# Tkinter GUI for the Travelling Salesperson Program. This GUI was created and tested using Windows.
# Hopefully it looks okay on Mac and Linux.

class TravelApp(tkinter.Tk):
    """ Main class for the GUI. Contains all other GUI elements. """

    def __init__(self, parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.travel_db = TravelDB()
        self.agent = TravelAgent(self.travel_db)
        self.inpt = InputHandler(self.travel_db)
        self.initialize()

    def initialize(self):
        basepadding = 2
        self.grid()
        self.minsize(width=350, height=250)
        self.resizable(False, False)    # Don't allow user to resize window.

        # The main app contains a Notebook widget that creates tabs along the top.
        # Each tab contains a Frame that is dedicated to one function of the program. 
        # Tabs/frames are: Cheapest Route, File Input, Search Airports, Flight Cost.
        self.nbook = ttk.Notebook(self)
        self.nbook.output_font = tkinter.font.Font(root=self.nbook, family="Courier New", size=11, weight="normal")
        self.cr_frame = CheapestRouteFrame(self.nbook, basepadding, self.travel_db, self.agent, self.inpt)
        self.fr_frame = FileRouteFrame(self.nbook, basepadding, self.travel_db, self.agent, self.inpt)
        self.as_frame = SearchFrame(self.nbook, basepadding, self.travel_db, self.agent, self.inpt)
        self.fc_frame = FlightCostFrame(self.nbook, basepadding, self.travel_db, self.agent, self.inpt)
        self.nbook.add(self.cr_frame, text=self.cr_frame.title)
        self.nbook.add(self.fr_frame, text=self.fr_frame.title)
        self.nbook.add(self.as_frame, text=self.as_frame.title)
        self.nbook.add(self.fc_frame, text=self.fc_frame.title)
        self.nbook.grid(sticky="nsew")
        # Make the notebook and window resize with content as necessary
        self.grid_columnconfigure(0, weight=1)
        self.nbook.grid_columnconfigure(0, weight=1)
        self.nbook.bind_all("<<NotebookTabChanged>>", self.tabChanged)  # Hides result boxes on tab change

    def tabChanged(self, event):
        """ Hide results boxes. Called when tab is changed. """
        self.fr_frame.hideResults()
        self.as_frame.hideResults()
        self.update()

# Uncomment below to test GUI directly
# app = TravelApp(None)
# app.title("Travelling Salesperson Calculator")
# app.mainloop()