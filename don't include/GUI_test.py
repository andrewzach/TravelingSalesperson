import tkinter
from tkinter import ttk
from traveldb import FileHandler, Airport, Country, Currency, TravelDB
from travelcalc import Itinerary, TravelAgent, Route

class TravelApp(tkinter.Tk):

    def __init__(self, parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

# n = ttk.Notebook(parent)
# f1 = ttk.Frame(n); # first page, which would get widgets gridded into it
# f2 = ttk.Frame(n); # second page
# n.add(f1, text='One')
# n.add(f2, text='Two')

    def initialize(self):
        self.grid()

        self.nbook = ttk.Notebook(self)
        self.testframe = ttk.Frame(self.nbook)
        self.testframe2 = ttk.Frame(self.nbook)
        self.nbook.add(self.testframe, text="One")
        self.nbook.add(self.testframe2, text="Two")
        self.nbook.grid(row=2)
        self.entryvar = tkinter.StringVar()
        self.entry = tkinter.Entry(self.testframe, textvariable=self.entryvar)
        self.entry.grid(column=0, row=0, sticky="EW")
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryvar.set("Enter text here")

        button = tkinter.Button(self.testframe, text="Calculate Distance", command=self.OnButtonClick)
        button.grid(column=1, row=0)

        self.labelvar = tkinter.StringVar()
        label = tkinter.Label(self.testframe, textvariable=self.labelvar, anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, columnspan=2, sticky="EW")
        self.labelvar.set("Hello!")

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

    def OnPressEnter(self, event):
        self.labelvar.set(self.entryvar.get()+ " You pressed enter!")

    def OnButtonClick(self):
        self.labelvar.set(self.entryvar.get()+ " You clicked the button!")

app = TravelApp(None)
app.title("Traveling Salesperson Calculator")

travel_db = TravelDB()
agent = TravelAgent(travel_db)

app.mainloop()



# def flightCost():
#     org = origin_code.get()
#     dst = dest_code.get()
#     cost.set(agent.flightCost(org,dst))

# origin_code = StringVar()
# dest_code = StringVar()
# cost = StringVar()

# Label(root, text="Origin").grid(row=0)
# Label(root, text="Destination").grid(row=1)
# Label(root, text="Result:").grid(row=2)
# Label(root, textvariable=cost).grid(row=2, column=1)
# origin_code = Entry(root)
# dest_code = Entry(root)
# origin_code.grid(row=0, column=1)
# dest_code.grid(row=1, column=1)
# button = Button(root, text='Calculate Cost', width=25, command=flightCost).grid(row=3)

# root.mainloop()