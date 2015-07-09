# Author:     Andrew Zacharias
# Student #:  D14127051
# Date:       May 2015

import csv
import os
from traveldb import Airport, Country, Currency

class InputHandler:

    def __init__(self, travel_db):
        self.travel_db = travel_db

    def airportCodeInput(self, prompt):
        """ Return an airport code input after validating it """
        while True:
            code = input(prompt).upper()
            if code not in self.travel_db.airports:
                print("Invalid airport code")
            else:
                return code

    def countryInput(self, prompt):
        """ Return a country name input after validating it """
        while True:
            name = input(prompt)
            if name not in self.travel_db.countries:
                print("Invalid country name. Please make sure name is capitalized.")
            else:
                return name

    def currencyInput(self, prompt):
        """ Return a currency code input after validaing it """
        while True:
            code = input(prompt).upper()
            if code not in self.travel_db.currencies:
                print("Invalid currency code")
            else:
                return code

    # Validate functions below were used for GUI input validation, 
    # but I have chosen other ways to handle that now.
    def validateAirport(self, code):
        """ Return True if airport code valid, False otherwise. """
        print(code)
        if code in self.travel_db.airports:
            return True
        else:
            return False

    def validateCountry(self, country_name):
        """ Return True if country_name valid, False otherwise. """
        if country_name in self.travel_db.countries:
            return True
        else:
            return False

    def validateCurrency(self, currency_code):
        """ Return True if currency_code valid, False otherwise. """
        if currency_code in self.travel_db.currencies:
            return True
        else:
            return False

class FileHandler:
    """ Handles file input and output, as well as the building of dictionaries for the TravelDB """

    # Dictionaries that are built will ignore airports with inconsistent country and currency values.
    # The .csv files have been corrected where possible to fix these inconsistencies, but a few remain.
    
    def buildCurrencyDict(filename):
        """ Return a dictionary of Currency objects, with key = currency code. Created from info stored in filename """ 
        currencies = {}
        with open(os.path.join("input", filename), "rt", encoding="utf8") as f:
            reader = csv.reader(f)
            for line in reader:
                currencies[line[1]] = Currency(line[1], line[0], float(line[2]))
        return currencies

    def buildCountryDict(filename, currencies_dict):
        """ Return a dictionary of Country objects, with key = country name. Created from info stored in filename """
        # This function requires the currency dictionary to be built already.
        countries = {}
        with open(os.path.join("input", filename), "rt", encoding="utf8") as f:
            reader = csv.reader(f)
            for line in reader:
                try:
                    countries[line[0]] = Country(line[0], line[14], currencies_dict)
                except KeyError:    # If currency isn't found, country won't be added to the dictionary
                    continue
        return countries

    def buildAirportDict(filename, countries_dict):
        """ Return a dictionary of Airport objects, with key = airport code. Created from info stored in filename """ 
        # This function requires the country dictionary to be built already.
        airports = {}
        with open(os.path.join("input", filename), "rt", encoding="utf8") as f:
            reader = csv.reader(f)
            for line in reader:
                try:
                    airports[line[4]] = Airport(line[4], line[1], line[3], line[2], float(line[6]), float(line[7]), countries_dict)
                except KeyError:    # If country isn't found, the airport won't be added to the dictionary
                    continue
        return airports

    def getRouteInputFile(filename):
        """ Return a list of routes from a file, in the format [name, [airport code list]]. Return None if file not found. """
        if filename[-4:] != ".csv":     # Make sure the filename is a .csv
            return None
        routes = []
        try:
            with open(os.path.join("input", filename), "rt", encoding="utf8") as f:
                reader = csv.reader(f)
                for line in reader:
                    try:
                        routes.append([line[0], line[1:]])
                    except (UnicodeDecodeError, IndexError):
                        # skip blank lines and lines with invalid characters
                        continue
        except (FileNotFoundError, OSError):
            return None
        return routes

    def writeRoutesCSV(filename, routes):
        """ Create a csv input file, given a list of routes. Routes are lists of names and airport codes. """
        if filename[-4:] != ".csv":     # Make sure the filename is a .csv
            filename += ".csv"
        try:
            with open(os.path.join("input", filename), "w", newline='') as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerows(routes)
        except (OSError, FileNotFoundError):
            return False
        else:
            return True

    def writeItineraryOutput(filename, itins):
        """ Write output .csv file for list of itineraries. Output file shows cheapest route and its cost. """
        if filename[-4:] != ".csv":     # Make sure the filename is a .csv
            filename += ".csv"
        try:
            with open(os.path.join("output", filename), "w", newline='') as f:
                writer = csv.writer(f, delimiter=",")
                firstline = ["Name", "Cost", "Home", "Dest 1", "Dest 2", "Dest 3", "Dest 4", "Dest 5", "Dest 6"]
                writer.writerow(firstline)
                for itinerary in itins:
                    line = []
                    line.append(itinerary.name)
                    line.append(itinerary.cheapest_cost)
                    line = line + itinerary.cheapest_route.getCodeList()
                    writer.writerow(line)
        except (FileNotFoundError, OSError):
            return False
        else: 
            return True

    def generateRandomInput(filename, num_people, travel_db):
        """ Create an input file with randomly generated routes for num_people. """
        import random
        routes = []
        for i in range(num_people):
            route = travel_db.randomRoute()
            route.insert(0,"Person " + str(i))  # Add a name for each route.
            routes.append(route)
        if FileHandler.writeRoutesCSV(filename,routes): # If it's successful writing the file
            print("File {0} created successfully with {1} people.".format(filename, num_people))
        else:
            print("File {0} could not be created.".format(filename))
