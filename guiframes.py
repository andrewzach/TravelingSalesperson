# Author:     Andrew Zacharias
# Student #:  D14127051
# Date:       May 2015

import tkinter
from tkinter import ttk
import tkinter.font
from inputoutput import FileHandler
import math

# This file contains all frames of the GUI interface. One Frame for each notebook tab option.
# Options are: Flight Costs, Cheapest Route, File Input, Search Airports.

class FlightCostFrame(ttk.Frame):

    def __init__(self, parent, basepadding, travel_db, agent, input_handler, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.travel_db = travel_db
        self.agent = agent
        self.inpt = input_handler
        self.title = "Flight Costs"
        self.bpad = basepadding
        self.initialize()

    def initialize(self):
        self.grid(sticky="ew")

        self.org_code = tkinter.StringVar()
        self.dst_code = tkinter.StringVar()
        self.cost_result = tkinter.StringVar()
        self.textoutput = tkinter.StringVar()

        tkinter.Label(self, text="Origin code: ").grid(column=0, row=0, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Destination code: ").grid(column=0, row=1, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Flight Cost: ").grid(column=0, row=3, sticky="ew")

        # Warning labels that display ! when invalid airport codes entered
        self.org_warning_label = WarningLabel(self)
        self.org_warning_label.grid(column=2, row=0)
        self.dst_warning_label = WarningLabel(self)
        self.dst_warning_label.grid(column=2, row=1)

        # Text entry boxes
        self.org_entry = tkinter.Entry(self, textvariable=self.org_code)
        self.org_entry.grid(column=1, row=0, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.dst_entry = tkinter.Entry(self, textvariable=self.dst_code)
        self.dst_entry.grid(column=1, row=1, sticky="ew", pady=self.bpad, padx=self.bpad)

        ttk.Separator(self, orient=tkinter.HORIZONTAL).grid(row=2, columnspan=3, stick="ew", pady=3)
        
        self.cost_out = tkinter.Label(self, textvariable=self.cost_result)
        self.cost_out.grid(column=1, row=3)

        # LabelFrame showing detailed information
        self.textoutframe = ttk.LabelFrame(self, text="Details")
        self.textoutframe.grid(row=5,columnspan=3, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.textout = tkinter.Label(self.textoutframe, textvariable=self.textoutput, height=3, justify="left")
        self.textout.grid()

        button = tkinter.Button(self, text="Calculate Cost", command=self.flightCost)
        button.grid(column=1, row=7)
        self.dst_entry.bind("<Return>", self.flightCost)

        self.grid_columnconfigure(0, weight=1)
        self.org_entry.focus_set()

    def flightCost(self, event=None):
        """ Calculate cost of flight based on form input. Display results """
        self.org_warning_label.reset()
        self.dst_warning_label.reset()
        self.textoutput.set("")

        origin = self.travel_db.getAirport(self.org_code.get())
        destination = self.travel_db.getAirport(self.dst_code.get())

        if origin and destination:
            cost = self.agent.calcFlightCost(origin, destination)
            distance = int(origin.distanceFrom(destination))
            output = "€ {cost:.2f}".format(**locals())
            self.textoutput.set("\tOrigin:\t\t{origin.name}\n\tDestination:\t{destination.name}\n\tDistance:\t{distance} km".format(**locals()))
            self.org_entry.focus_set()
            self.org_entry.selection_range(0, tkinter.END)
        elif not origin:
            output = "Invalid origin"
            self.org_warning_label.trigger()
            self.org_entry.focus_set()
            self.org_entry.selection_range(0, tkinter.END)
        elif not destination:
            output = "Invalid destination"
            self.dst_warning_label.trigger()
            self.dst_entry.focus_set()
            self.dst_entry.selection_range(0, tkinter.END)

        self.cost_result.set(output)

class CheapestRouteFrame(ttk.Frame):

    def __init__(self, parent, basepadding, travel_db, agent, input_handler, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.travel_db = travel_db
        self.agent = agent
        self.inpt = input_handler
        self.title = "Cheapest Route"
        self.bpad=basepadding
        self.map_win = None
        self.initialize()

    def initialize(self):
        self.grid()

        self.home_code = tkinter.StringVar()
        self.dst1_code = tkinter.StringVar()
        self.dst2_code = tkinter.StringVar()
        self.dst3_code = tkinter.StringVar()
        self.dst4_code = tkinter.StringVar()
        self.textoutput = tkinter.StringVar()

        # Labels for text entry
        tkinter.Label(self, text="Home Airport: ").grid(column=0, row=0, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Destination 1: ").grid(column=0, row=1, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Destination 2: ").grid(column=0, row=2, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Destination 3: ").grid(column=0, row=3, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Destination 4: ").grid(column=0, row=4, sticky="ew", pady=self.bpad, padx=self.bpad)

        # Text entry boxes
        self.home_entry = tkinter.Entry(self, textvariable=self.home_code)
        self.home_entry.grid(column=1, row=0, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.dst1_entry = tkinter.Entry(self, textvariable=self.dst1_code)
        self.dst1_entry.grid(column=1, row=1, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.dst2_entry = tkinter.Entry(self, textvariable=self.dst2_code)
        self.dst2_entry.grid(column=1, row=2, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.dst3_entry = tkinter.Entry(self, textvariable=self.dst3_code)
        self.dst3_entry.grid(column=1, row=3, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.dst4_entry = tkinter.Entry(self, textvariable=self.dst4_code)
        self.dst4_entry.grid(column=1, row=4, sticky="ew", pady=self.bpad, padx=self.bpad)

        ttk.Separator(self, orient=tkinter.HORIZONTAL).grid(row=5, columnspan=2, sticky="ew", pady=3)
        # Displays output
        self.textout = tkinter.Label(self, textvariable=self.textoutput, height=3, justify="left")
        self.textout.grid(row=6, columnspan=2)

        ttk.Separator(self, orient=tkinter.HORIZONTAL).grid(row=7, columnspan=2, sticky="ew", pady=3)

        # Buttons
        button = tkinter.Button(self, text="Calculate Route", command=self.cheapestRoute)
        button.grid(column=1, row=8)
        self.rand_button = tkinter.Button(self, text="Generate Random Route", command=self.genRandomRoute)
        self.rand_button.grid(column=0, row=8, sticky="w")
        self.map_button = tkinter.Button(self, text="View Map", command=self.viewMap)

        self.dst4_entry.bind("<Return>", self.cheapestRoute)    # Hitting return after last route runs calculation.
        self.grid_columnconfigure(0, weight=1)
        self.home_entry.focus_set()

    def cheapestRoute(self, event=None):
        """ Calculate cheapest route based on form input. Display results. """
        self.textoutput.set("")

        home = self.home_code.get()
        dst1 = self.dst1_code.get()
        dst2 = self.dst2_code.get()
        dst3 = self.dst3_code.get()
        dst4 = self.dst4_code.get()
        
        self.cheapest_itin = self.agent.cheapestRoute([home,dst1,dst2,dst3,dst4])
        if self.cheapest_itin:
            self.textoutput.set(self.cheapest_itin.getStringGUI())
            self.map_button.grid(column=0, row=8, sticky="e")
            if self.map_win:    # If map is already open, plot the map.
                self.viewMap()
            self.home_entry.focus_set()
            self.home_entry.selection_range(0, tkinter.END)
        else:
            self.map_button.grid_forget()
            self.textoutput.set("Error: One or more airport codes invalid.")
            # Note: It would be nice to validate all the codes individually, but it takes too much code to be worth it.

    def genRandomRoute(self):
        """ Generate random routes and fills in form with the airport codes. Run calculation after. """
        route_codes = self.travel_db.randomRoute()
        self.home_code.set(route_codes[0])
        self.dst1_code.set(route_codes[1])
        self.dst2_code.set(route_codes[2])
        self.dst3_code.set(route_codes[3])
        self.dst4_code.set(route_codes[4])
        self.cheapestRoute()

    def viewMap(self):
        """ Open a new window displaying map of cheapest route """
        if not self.map_win:    # Create map window if it doesn't exist
            self.map_win = MapWindow(self, title="Travelling Salesperson - Cheapest Route Map")
        self.map_win.clearMap()
        self.map_win.plotCheapItinerary(self.cheapest_itin)
        self.map_win.focus_set()

class FileRouteFrame(tkinter.Frame):

    def __init__(self, parent, basepadding, travel_db, agent, input_handler, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.travel_db = travel_db
        self.agent = agent
        self.inpt = input_handler
        self.title = "File Input"
        self.bpad=basepadding
        self.results_avail = False
        self.initialize()

    def initialize(self):
        self.grid()

        self.file_in = tkinter.StringVar()
        self.file_out = tkinter.StringVar()
        self.print_option = tkinter.IntVar()
        self.print_option.set(True)
        self.textoutput = tkinter.StringVar()

        # Input Labels
        tkinter.Label(self, text="Input File: ").grid(column=0, row=0, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Output File (optional): ").grid(column=0, row=1, sticky="ew", pady=self.bpad, padx=self.bpad)

        # Text entry fields
        self.file_in_entry = tkinter.Entry(self, textvariable=self.file_in)
        self.file_in_entry.grid(column=1, row=0, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.file_out_entry = tkinter.Entry(self, textvariable=self.file_out)
        self.file_out_entry.grid(column=1, row=1, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.print_option_check = tkinter.Checkbutton(self, text="Display Results", variable=self.print_option, onvalue=True, offvalue=False)
        self.print_option_check.grid(column=1, row=2, pady=self.bpad, padx=self.bpad)

        # Details frame
        self.textoutframe = ttk.LabelFrame(self, text="Details")
        self.textoutframe.grid(row=3,columnspan=2, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.textout = tkinter.Label(self.textoutframe, textvariable=self.textoutput, height=2, justify="left")
        self.textout.grid(row=0)

        button = tkinter.Button(self, text="Process Routes", command=self.fileCheapestRoutes)
        button.grid(column=1, row=4)

        # Results out box, displaying the output. This will appear to the right of the window after results are calculated.
        self.resultsout = tkinter.Text(self, height=10, width=50, wrap="none", font=self.parent.output_font, bg="#272822", fg="#f8f8f2")
        self.resultsout.tag_configure('number', foreground="#ae81ef")   # Tags to change color of text in results
        self.resultsout.tag_configure('route', foreground="#e6db74")
        self.scroll = tkinter.Scrollbar(self, command=self.resultsout.yview)
        self.resultsout.configure(yscrollcommand=self.scroll.set)
        self.hideresults = tkinter.Button(self, text="<< Hide", command=self.hideResults)
        self.showresults = tkinter.Button(self, text="Show Results >>", command=self.showResults)

        # Makes hittin Return calculate the cheapest routes
        self.file_in_entry.bind("<Return>", self.fileCheapestRoutes)
        self.file_out_entry.bind("<Return>", self.fileCheapestRoutes)

        self.grid_columnconfigure(0, minsize=200)
        self.grid_columnconfigure(3, weight=1)
        self.file_in_entry.focus_set()

    def fileCheapestRoutes(self, event=None):
        """ Calculate cheapest routes from csv file entered in text entry. Display results as requested. """
        self.textoutput.set("Processing...")
        self.resultsout.delete(1.0, tkinter.END) # Delete any previous results
        self.update()
        fileinput = self.file_in.get()
        fileoutput = self.file_out.get()    # None if left blank
        printoption = self.print_option.get()
        file_routes = FileHandler.getRouteInputFile(fileinput)
        if not file_routes:
            self.textoutput.set("Filename not found")
            return

        result_itins, errors = self.agent.cheapestRoutesFromFile(file_routes, printout=False, fileout=fileoutput)
        if result_itins:    # If calculations were successful
            self.results_avail = True
            num_results = len(result_itins)
            num_errors = len(errors)
            self.textoutput.set("Successfully processed {0} routes. ({1} errors)".format(num_results, num_errors))
            if printoption:
                self.showResults()
                for itin in result_itins:
                    # Prints results in box to the right. Uses custom tags for font color. 
                    self.resultsout.insert(tkinter.END, "{name:15s}".format(name=itin.name))
                    self.resultsout.insert(tkinter.END, "\t{route}\n".format(route=itin.route.getSimpleString()), "route")
                    self.resultsout.insert(tkinter.END, "Cheapest Route:")
                    self.resultsout.insert(tkinter.END, "\t{cheap_route:50s}\n".format(cheap_route=itin.cheapest_route.getSimpleString()), "route")
                    self.resultsout.insert(tkinter.END, "Cost: € ")
                    self.resultsout.insert(tkinter.END, str(itin.cheapest_cost) + "\n\n", "number")
                if errors:
                    self.resultsout.insert(tkinter.END, "\nErrors: {num_errors} with routes.\n-------------\n".format(num_errors=num_errors))
                    for error in errors:
                        self.resultsout.insert(tkinter.END, error + "\n")
            else:   # If not displaying results, remove results box.
                self.resultsout.grid_forget()
                self.scroll.grid_forget()
                self.hideresults.grid_forget()
                self.showresults.grid_forget()
        else:
            self.results_avail = False
            self.textoutput.set("Error processing routes")
        self.update()

    def hideResults(self):
        """ Hide results box to the right of the window. """
        self.resultsout.grid_forget()
        self.scroll.grid_forget()
        self.hideresults.grid_forget()
        if self.results_avail:  # If results are available, still show the "Show Results >>" button
            self.showresults.grid(row=5, column=1)
        else:
            self.showresults.grid_forget()

    def showResults(self):
        """ Show results box to the right of the window. """
        self.resultsout.grid(row=0, column=3, rowspan=5)
        self.scroll.grid(row=0, column=4, rowspan=5, sticky="ns")
        self.hideresults.grid(row=5, column=3)
        self.showresults.grid_forget()

class SearchFrame(tkinter.Frame):

    def __init__(self, parent, basepadding, travel_db, agent, input_handler, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.travel_db = travel_db
        self.agent = agent
        self.inpt = input_handler
        self.title = "Search Airports"
        self.bpad=basepadding
        self.results_avail = False
        self.map_win = None
        self.initialize()

    def initialize(self):
        self.grid()

        self.name = tkinter.StringVar()
        self.code = tkinter.StringVar()
        self.country = tkinter.StringVar()
        self.city = tkinter.StringVar()
        self.textoutput = tkinter.StringVar()

        # Labels for text entry fields
        tkinter.Label(self, text="Name: ").grid(column=0, row=0, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Airport Code: ").grid(column=0, row=1, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="Country: ").grid(column=0, row=2, sticky="ew", pady=self.bpad, padx=self.bpad)
        tkinter.Label(self, text="City: ").grid(column=0, row=3, sticky="ew", pady=self.bpad, padx=self.bpad)

        # Text entry fields
        self.name_entry = tkinter.Entry(self, textvariable=self.name)
        self.name_entry.grid(column=1, row=0, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.code_entry = tkinter.Entry(self, textvariable=self.code)
        self.code_entry.grid(column=1, row=1, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.country_entry = tkinter.Entry(self, textvariable=self.country)
        self.country_entry.grid(column=1, row=2, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.city_entry = tkinter.Entry(self, textvariable=self.city)
        self.city_entry.grid(column=1, row=3, sticky="ew", pady=self.bpad, padx=self.bpad)
        
        # Details frame
        self.textoutframe = ttk.LabelFrame(self, text="Details")
        self.textoutframe.grid(row=4,columnspan=2, sticky="ew", pady=self.bpad, padx=self.bpad)
        self.textout = tkinter.Label(self.textoutframe, textvariable=self.textoutput, height=2, justify="left")
        self.textout.grid(row=0)

        button = tkinter.Button(self, text="Search Airports", command=self.searchAirports)
        button.grid(column=1, row=5)

        # Results out box. Displays to the right of the window after results are found.
        self.resultsout = tkinter.Text(self, height=10, width=100, wrap="none", font=self.parent.output_font, bg="#272822", fg="#f8f8f2")
        self.resultsout.tag_configure('label', foreground="#ae81ef")
        self.scroll = tkinter.Scrollbar(self, command=self.resultsout.yview)
        self.resultsout.configure(yscrollcommand=self.scroll.set)
        self.hideresults = tkinter.Button(self, text="<< Hide", command=self.hideResults)
        self.showresults = tkinter.Button(self, text="Show Results >>", command=self.showResults)
        self.mapresults = tkinter.Button(self, text="View Map", command=self.viewMap)

        # Make the program search when the user hits Return
        self.name_entry.bind("<Return>", self.searchAirports)
        self.code_entry.bind("<Return>", self.searchAirports)
        self.country_entry.bind("<Return>", self.searchAirports)
        self.city_entry.bind("<Return>", self.searchAirports)

        self.grid_columnconfigure(0, minsize=200)
        self.grid_columnconfigure(3, weight=1)
        self.name_entry.focus_set()

    def viewMap(self):
        """ Display a map of the search results. """
        # Create map window if it doesn't exist
        if not self.map_win:
            self.map_win = MapWindow(self, title="Travelling Salesperson - Airport Search Results")
        self.map_win.clearMap() # Clear previous results from map
        # Don't label airport codes if more than 40 results being shown to avoid clutter.
        label = False if len(self.airports_found) > 40 else True
        for apt in self.airports_found:
            self.map_win.plotAirport(apt, label)
        self.map_win.focus_set()

    def searchAirports(self, event=None):
        """ Search airports database based on criteria entered in entry widgets. Display results. """
        self.textoutput.set("Searching...")
        self.resultsout.delete(1.0, tkinter.END) # Delete any previous results
        self.update()
        name = self.name.get()
        code = self.code.get()
        country = self.country.get()
        city = self.city.get()

        self.airports_found = self.travel_db.searchAirports(code=code, country_name=country, city=city, name=name)
        if self.airports_found[0]:  # If results were found
            self.airports_found.sort(key=lambda airport: airport.country.name)   # Sort results by country
            num_results = str(len(self.airports_found))
            self.textoutput.set(num_results + " airports matching your search criteria found.")
            self.results_avail = True   # Ensures "Show Results >>" button will be displayed
            self.showresults.grid(row=6, column=1)  # Display "Show Results >>" button
            self.mapresults.grid(column=0, row=5)   # Display "View Map" button
            for airport in self.airports_found:
                # Displays the results in the box to the right. Text is formatted with tags for color.
                self.resultsout.insert(tkinter.END, "Name: ", "label")
                self.resultsout.insert(tkinter.END, "{name:25.25s} ".format(name=airport.name))
                self.resultsout.insert(tkinter.END, "Loc: ", "label")
                self.resultsout.insert(tkinter.END, "{location:25.25s} ".format(location=airport.country.name + " - " + airport.city))
                self.resultsout.insert(tkinter.END, "Code: ", "label")
                self.resultsout.insert(tkinter.END, "{code}\t".format(code=airport.code))
                self.resultsout.insert(tkinter.END, "Lat: ", "label")
                self.resultsout.insert(tkinter.END, "{lat:7.3f}\t".format(lat=airport.latitude))
                self.resultsout.insert(tkinter.END, "Long: ", "label")
                self.resultsout.insert(tkinter.END, "{long:7.3f}\n".format(long=airport.longitude))
        else:
            self.results_avail = False
            self.hideResults()
            self.mapresults.grid_forget()
            self.textoutput.set("0 results found.")
        self.update()

    def hideResults(self):
        """ Hide the results box on the right of the window """
        self.resultsout.grid_forget()
        self.scroll.grid_forget()
        self.hideresults.grid_forget()
        if self.results_avail:      # Display "Show Results >>" button if results are available.
            self.showresults.grid(row=6, column=1)
        else:
            self.showresults.grid_forget()

    def showResults(self):
        """ Show the results box to the right of the window """
        self.resultsout.grid(row=0, column=3, rowspan=5)
        self.scroll.grid(row=0, column=4, rowspan=5, sticky="ns")
        self.hideresults.grid(row=6, column=3)
        self.showresults.grid_forget()


class WarningLabel(tkinter.Label):
    """ Used to create warning labels (!) for text boxes with invalid or missing information. """

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.triggered = False
        self.display = tkinter.StringVar()
        tkinter.Label.__init__(self, parent, textvariable=self.display, fg="red", *args, **kwargs)

    def trigger(self):
        """ Change label to ! """
        self.triggered = True
        self.display.set("!")

    def reset(self):
        """ Reset label to blank """
        self.triggered = False
        self.display.set("")


# Map window popup used to map routes and airports
# The map is 1080 x 540 px. It is an equirectangular projection making 1° lat/long = 3 px. 
# Note: I figured all this stuff out by myself... Considered using matplotlib but didn't want user to have to install it.
class MapWindow(tkinter.Toplevel):
    """ A popup window containing a Canvas used to display a map. Can plot airports and flights on map. """

    def __init__(self, parent, title="Travelling Salesperson - Map"):
        tkinter.Toplevel.__init__(self, parent)
        self.parent = parent
        self.resizable(False, False)    # Plotting is based on pixels. Map cannot be resized.
        self.airport_markers = {}
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.windowClose)     # Called upon window close
        self.initialize()

    def initialize(self):
        self.map_canvas = tkinter.Canvas(self, width=1080, height=540, highlightthickness=0)
        self.mapfile = tkinter.PhotoImage(file="worldmap1080v2.gif")
        self.mapimage = self.map_canvas.create_image(540, 270, image=self.mapfile)
        self.map_canvas.grid()

    def windowClose(self):
        """ Called when user presses X on window. Informs parent window that map has been closed. """
        self.parent.map_win = None # Inform parent that map has been closed and doesn't exist anymore
        self.destroy()

    def clearMap(self):
        """ Deletes all markers and plotted routes from the map """
        self.map_canvas.delete("all")
        self.mapimage = self.map_canvas.create_image(540, 270, image=self.mapfile)
        self.update()

    def plotCheapItinerary(self, itin):
        """ Plot an Itinerary's cheapest route on the map """
        airports = itin.cheapest_route.airports
        for i in range(len(airports)-1):
            self.plotFlight(airports[i], airports[i+1])
        for apt in airports:
            self.plotAirport(apt)

    def plotAirport(self, airport, label=True):
        """ Plot airport on the map as a circle. Label with airport code option """
        x = self.longToX(airport.longitude)
        y = self.latToY(airport.latitude)
        self.map_canvas.create_oval(x-3, y-3, x+3, y+3, fill="purple")
        if label:
            self.map_canvas.create_text(x,y+10,fill="white",font=self.parent.parent.output_font,text=airport.code)

    def plotFlight(self, apt1, apt2):
        """ Plot a flight as a line drawn between two airports """
        x1 = self.longToX(apt1.longitude)
        y1 = self.latToY(apt1.latitude)
        x2 = self.longToX(apt2.longitude)
        y2 = self.latToY(apt2.latitude)

        # Below code checks if route will need to go over the edge of the map. 
        # If x distance is greater than half the world, then show route going over edge of map.
        # The appropriate slope is calculated between the airports, crossing the 180th meridian. 
        # Two lines are plotted. One from the origin to the edge, and one from the other edge to the destination.
        if abs(x2-x1) > 540:
            if x2 > 540:    # flying over left edge
                slope = (y2-y1)/(x1+(1080-x2))
                self.map_canvas.create_line(x1, y1, 0, y1 + (x1 * slope), fill="orange", width=2) # from origin to left edge
                self.map_canvas.create_line(1080, y1 + (x1 * slope), x2, y2, fill="orange", width=2) # from right edge to destination
            else:           # flying over right edge
                slope = (y2-y1)/(x2+(1080-x1))
                self.map_canvas.create_line(x1, y1, 1080, y1 + ((1080-x1) * slope), fill="orange", width=2) # from origin to right edge
                self.map_canvas.create_line(0, y1 + ((1080-x1) * slope), x2, y2, fill="orange", width=2) # from left edge to destination
        else:
            # Default behavior. Just plots direct line between airports.
            self.map_canvas.create_line(x1, y1, x2, y2, fill="orange", width=2)

    # Converts latitude to y-coordinates, with top of the window/world = 0. 1°lat = 3px
    def latToY(self, latitude):
        """ Transform latitude into y-coordinate (map height 540px) Return y-coord """
        y_coord = 540 - ((latitude + 90) * 3)   # 540 = height of map
        return int(round(y_coord))

    # Converts longitude to x-coordinates, with left sisde of the window = 0. 1°long = 3px
    def longToX(self, longitude):
        """ Transform longitude into x-coordinate (map width 1080px). Return x-coord """
        x_coord = (longitude + 180) * 3
        return int(round(x_coord))