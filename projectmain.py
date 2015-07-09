# DT265: Object Oriented Software Development 1
# Travelling Salesperson Project
# Author:     Andrew Zacharias
# Student #:  D14127051
# Date:       May 2015

# Note: All input files must be located in the input/ directory of the project.
# Output files will be placed in the output/ directory.

from traveldb import Airport, Country, Currency, TravelDB
from travelcalc import Itinerary, TravelAgent, Route
from inputoutput import InputHandler, FileHandler
from traveltesting import Tester, Benchmarker
from maingui import TravelApp
import time

def displayMenu():
    print()
    print("##############################")
    print("############ MENU ############")
    print("##############################")
    print("A. Airport Info")
    print("C. Country Info")
    print("D. Distance Calculator")
    print("R. Cheapest Route")
    print("F. Flight Cost")
    print("S. Airport Search")
    print("I. File Input - Cheapest Route")
    print("G. Generate Random Input File")
    print("T. Run Automatic Tests")
    print("B. Run Program Benchmarks")
    print("L. Launch GUI Program")
    print("?. Program Information")
    print("Q. Quit")

def getMenuSelection():
    menu_options = ('A','C','D','R','F','S','I','G','T','B','L','?','Q')
    displayMenu()
    choice = input("> ").upper()
    while choice not in menu_options:
        print("Invalid input")
        displayMenu()
        choice = input("> ").upper()
        print()
    return choice

### ?. Program Information
def programInfo():
    print("###############################################################################")
    print("###################### Travelling Executive Salesperson #######################")
    print("###################### Travel Inventory Navigation Guide ######################")
    print("###############################################################################")
    print("|                              Program Information                            |")
    print("|-----------------------------------------------------------------------------|")
    print("|                                                                             |")
    print("| Each month, a salesperson needs to leave their home city and visit          |")
    print("| prospective customers in 4 other cities. At the end of the month they must  |")
    print("| return to their home city. They can take a maximum of 6 flights in one      |")
    print("| month. This program is designed to help optimize their routes among the 5   |")
    print("| cities to yield the cheapest possible route. Sometimes this will involve    |")
    print("| making an extra stop at a city already visited.                             |")
    print("|                                                                             |")
    print("| This program has two modes, the console mode (default) and a graphical user |")
    print("| interface (GUI) mode. To launch the GUI mode, select option L from the main |")
    print("| menu.                                                                       |")
    print("|                                                                             |")
    print("| All aiports must be input by their 3 letter codes. If you don't know a      |")
    print("| code, use the Search Airports option to find it.                            |")
    print("|                                                                             |")
    print("| This program accepts file input to calculate routes for multiple            |")
    print("| salespeople at once. Each file should be a .csv file. Each row should start |")
    print("| with the salesperson's name, followed by their home airport code, then the  |")
    print("| 4 airports they must visit. Input files must be located in the /input/      |")
    print("| folder in the program's directory. Output files will be created in the      |")
    print("| /output/ folder.                                                            |")
    print("|_____________________________________________________________________________|")

### A. Airport Info
def airportInfo():
    print("Enter the 3 letter IATA code for the airport.")
    airport_code = inpt.airportCodeInput("Airport Code: ")
    airport = travel_db.getAirport(airport_code)
    print("Info on", airport.name)
    print(airport)

### D. Distance Calculator
def airportDistance():
    print("----DISTANCE CALCULATOR----")
    airport_code1 = inpt.airportCodeInput("Airport Code 1: ")
    airport_code2 = inpt.airportCodeInput("Airport Code 2: ")
    airport1 = travel_db.getAirport(airport_code1)
    airport2 = travel_db.getAirport(airport_code2)
    print("Distance between", airport1.name, "and", airport2.name, "is", int(airport1.distanceFrom(airport2)), "km")

### C. Country Info
def countryInfo():
    print("----COUNTRY INFO----")
    country_name = inpt.countryInput("Country Name: ")
    print(agent.getCountryInfo(country_name))

### F. Flight Costs
def flightCosts():
    print("---- Flight Costs ----")
    origin_code = inpt.airportCodeInput("Origin: ")
    dest_code = inpt.airportCodeInput("Destination: ")
    origin = travel_db.getAirport(origin_code)
    destination = travel_db.getAirport(dest_code)
    cost = agent.calcFlightCost(origin, destination)
    distance = int(origin.distanceFrom(destination))
    print("Origin: {origin.name}\nDestination: {destination.name}\nDistance: {distance} km\nCost: €{cost:.2f}".format(**locals()))

### R. Cheapest Route
def cheapestRoutes():
    print("----CHEAPEST ROUTE----")
    print("Enter the IATA codes for the 5 airports in your route, starting with the home airport.")
    route_codes = []
    route_codes.append(inpt.airportCodeInput("Home: "))
    route_codes.append(inpt.airportCodeInput("Airport 1: "))
    route_codes.append(inpt.airportCodeInput("Airport 2: "))
    route_codes.append(inpt.airportCodeInput("Airport 3: "))
    route_codes.append(inpt.airportCodeInput("Airport 4: "))
    cheapest_itin = agent.cheapestRoute(route_codes)
    print(cheapest_itin)

### S. Search Airports 
def airportSearch():
    print("-----AIRPORT SEARCH-----")
    print("Search airports by a combination of name, airport code, country, and city.\nAll are optional. Press enter to skip a search term.")
    name = input("Name: ")
    airport_code = input("Airport Code: ")
    country = input("Country: ")
    city = input("City: ")

    airports_found = travel_db.searchAirports(code=airport_code, country_name=country, city=city, name=name)
    airports_found.sort(key=lambda airport: airport.country.name)   # Sort results by country
    print()
    print("----RESULTS----")
    for airport in airports_found:
        print(airport)

### I. File Input - Cheapest Routes
def fileInputCheapestRoutes():
    print("---- CHEAPEST ROUTES BY FILE INPUT -----")
    routes = None
    while not routes:
        filename = input("Filename: ")
        routes = FileHandler.getRouteInputFile(filename)
        if not routes:
            print("File not found or not a correctly formatted .csv.")
            print("Make sure input file is located in the /input/ directory")
    outfile = input("Output filename (optional): ")
    print()
    agent.cheapestRoutesFromFile(routes, fileout=outfile)

### G. Generate Random Input File
def generateRandomInput():
    print("---- GENERATE RANDOM INPUT FILE -----")
    filename = input("Filename: ")
    num_people = int(input("Number of people: "))
    FileHandler.generateRandomInput(filename, num_people, travel_db)

### T. Run Tests
def runAutomaticTests():
    print("----- AUTOMATIC TESTS -----")
    print()
    test = Tester(travel_db, agent, inpt)
    all_results = test.runAllTests()
    for result in all_results:
        print("{testname:32.32s}: {result}\t{info}\n".format(testname=result[0], result=result[1], info=result[2]))

### B. Run Program Benchmarks
def runProgramBenchmarks():
    print("----- PROGRAM BENCHMARKS -----")
    print()
    bench = Benchmarker(travel_db, agent)
    bench.benchmarkCheapestRoutes()

### L. Launch GUI
def launchGUI():
    print("---- GRAPHICAL USER INTERFACE ----")
    time.sleep(0.1)
    print("Launching GUI window...")
    time.sleep(0.2)
    app = TravelApp(None)
    app.title("Travelling Salesperson Calculator")
    # Below is fix for app window not having focus. It minimizes the window and then re-opens it.
    app.iconify()
    app.update()
    app.deiconify()

    app.mainloop()

# START OF MAIN PROGRAM
try:
    travel_db = TravelDB()
    agent = TravelAgent(travel_db)
    inpt = InputHandler(travel_db)
except Exception as e:
    print("Error initializing program.")
    print(e.__class__.__name__, ": ", e)
else:
    menu = {"A": airportInfo,
            "C": countryInfo,
            "D": airportDistance,
            "R": cheapestRoutes,
            "F": flightCosts,
            "S": airportSearch,
            "I": fileInputCheapestRoutes,
            "G": generateRandomInput,
            "T": runAutomaticTests,
            "B": runProgramBenchmarks,
            "L": launchGUI,
            "?": programInfo}
    time.sleep(0.1) # Makes menu display properly in Sublime Text 2
    choice = getMenuSelection()
    while choice != "Q":
        print()
        menu[choice]()      # Run the function corresponding to user's choice
        print()
        input("Press Enter to return to the main menu")
        choice = getMenuSelection()
print("Goodbye.")

