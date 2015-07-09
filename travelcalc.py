# Author:     Andrew Zacharias
# Student #:  D14127051
# Date:       May 2015

import itertools
import time

class Route:
    """ Contains a list of airport codes for a route """
    def __init__(self, airport_list):
        self.airports = airport_list

    def __str__(self):
        route_string = "'"
        for airport in self.airports:
            route_string += airport.code + "  "
        route_string = route_string[:-2]    # Delete last two spaces
        route_string += "'"
        return route_string

    def __eq__(self, other):
        if isinstance(other, Route):
            if self.airports == other.airports:
                return True
        return False

    def getSimpleString(self):
        """ Return a string of airport codes """
        route_string = ""
        for airport in self.airports:
            route_string += airport.code + "  "
        route_string = route_string[:-2]    # Delete last two spaces
        return route_string

    def getCodeList(self):
        """ Return a list of airport codes in the route """
        code_list = []
        for apt in self.airports:
            code_list.append(apt.code)
        return code_list

    def addReturnToHome(self):
        """ Append home airport (first one) to end of route """
        if self.airports[-1] != self.airports[0]:
            self.airports.append(self.airports[0])


class Itinerary:
    def __init__(self, route, name="Route"):
        self.home = route.airports[0]
        self.route = route
        self.route.addReturnToHome() # Appends home airport onto end of route.
        self.name = name
        # The below attributes are calculated later when needed.
        self.permutations = []
        self.cheapest_route = None
        self.cheapest_cost = None

    def setCheapestRoute(self, route, cost):
        self.cheapest_route = route
        self.cheapest_cost = cost

    def __str__(self):
        routestr = str(self.route)
        if self.cheapest_route:
            cheapest_routestr = str(self.cheapest_route)
            return "{self.name:17s}\t{routestr}\nCheapest Route:  \t{cheapest_routestr:40s}\tCost: € {self.cheapest_cost}\n".format(**locals())
        else:
            return "{self.name:17s}\t{routestr}\n".format(**locals())

    def getStringGUI(self):
        """ Return a string representation of an itinerary designed for the GUI """
        routestr = self.route.getSimpleString()
        cheapest_routestr = self.cheapest_route.getSimpleString()
        return "{self.name:15s}\t{routestr}\nCheapest Route:\t{cheapest_routestr:35s}\nCost: € {self.cheapest_cost}".format(**locals())

    def buildPermutations(self):
        """ Calculate all permutations of the route, including extra stop. Store them within this object as self.permutations. """
        ext_airport_list = []           # A list of airport code lists (routes). First route is basic one, others will have extra stop.
        ext_airport_list.append(self.route.airports[1:-1]) # Add original route with no extra stop. Remove the home city
        for apt in self.route.airports:
            extra_stop = self.route.airports[1:-1]  # original route without home city home city
            extra_stop.append(apt)                  # add an extra stop
            ext_airport_list.append(extra_stop)     # add new route with extra stop. One for each airport in original list.

        all_permutations = []
        for i in ext_airport_list:
            permutations = itertools.permutations(i)
            permutations = list(list(x) for x in permutations) # Convert tuple of tuple to a list of lists

            # This loop removes all permutations where the same airport is visited twice in a row.
            # First removes all permutations where home city is at beginning or end
            # Then removes any permutations where a city is repeated twice in a row
            # Iterates over the list backwards, starting at the end. Allows deleting elements from same list while iterating.
            if len(self.route.airports) < 7: # Performance is hindered for routes of more than 6 airports.             
                for i in reversed(range(len(permutations))):
                    perm = permutations[i]
                    if perm[0] == self.home or perm[-1] == self.home:
                        del permutations[i]
                        continue
                    for j in range(len(perm)-1):
                        if perm[j] == perm[j+1]:
                            del permutations[i]
                            break
            all_permutations += permutations

        all_perm_routes = []
        for perm in all_permutations:
            perm.insert(0, self.home)    # Insert home city at the beginning and end of each permutation
            perm.append(self.home)
            all_perm_routes.append(Route(perm))

        self.permutations = all_perm_routes


class TravelAgent:
    """ A controller class that performs calculations using objects within a TravelDB. """
    # This class is the one the user will interact with the most. Does everything related to flight and route costs.
    def __init__(self, travel_db):
        self.travel_info = travel_db

    # "calc" functions are generally used internally to calculate results. 
    # They take objects (Airports, Routes, Itineraries, etc.) as arguments.

    def calcFlightCost(self, origin, destination):
        """ Return cost of flight between Airports """
        distance = origin.distanceFrom(destination)
        cost = distance * origin.country.currency.toEuro()
        return cost

    def calcRouteCost(self, route):
        """ Return total cost of route """
        total_cost = 0
        for i in range(len(route.airports)-1):
            total_cost += self.calcFlightCost(route.airports[i], route.airports[i+1])
        return int(total_cost)

    def calcCheapestRoute(self, route_itin):
        """ Calculate the cheapest route for given itinerary, update it with results, and return the itinerary. """
        route_itin.buildPermutations()
        cost_matrix = self.calcCostMatrix(route_itin.route)
        # The default cheapest route is original one. This loops through each permutation and stores the route
        # with the cheapest cost in cheapest_route and cheapest_cost.
        cheapest_route = route_itin.route   
        cheapest_cost = self.routeCostFromMatrix(route_itin.route, cost_matrix)
        for route in route_itin.permutations:
            cost = self.routeCostFromMatrix(route, cost_matrix)
            # print(route, "\t€", cost)  # Uncomment while debugging to see all permutations.
            if cost < cheapest_cost:
                cheapest_route = route
                cheapest_cost = cost
        route_itin.setCheapestRoute(cheapest_route, cheapest_cost)
        return route_itin

    def buildRoute(self, route_codes):
        """ Create and return a Route object for a given list of airport codes """
        airport_list = []
        try:
            for code in route_codes:
                airport_list.append(self.travel_info.airports[code.upper()])
        except KeyError as e:
            return None

        return Route(airport_list)

    # Creates a matrix of all prices for all combination of flights between airports in a route.
    # This is used for more efficient price lookup. Greatly improves performance of cheapest route calcs.    
    def calcCostMatrix(self, route):
        """ Return a dictionary matrix of flight costs between all airports in Route object, with airport codes as keys. """
        cost_matrix = {}
        for org_apt in route.airports:
            cost_matrix[org_apt.code] = {}
            for dst_apt in route.airports:
                cost_matrix[org_apt.code][dst_apt.code] = self.calcFlightCost(org_apt, dst_apt)
        return cost_matrix

    # Alternative to calcRouteCost(), uses a cost_matrix to make it more efficient.
    def routeCostFromMatrix(self, route, cost_matrix):
        """ Return cost for entire route based on a cost_matrix. """
        total_cost = 0
        for i in range(len(route.airports)-1):
            total_cost += cost_matrix[route.airports[i].code][route.airports[i+1].code]
        return int(total_cost)
        
    # The functions below are what outside code usually interacts with. 
    # They take strings as input and look up the appropriate object in travel_db

    def flightCost(self, origin_code, destination_code):
        """Calculate cost of flight between airports, with airport code arguments. Return cost. """
        try:
            origin = self.travel_info.airports[origin_code]
        except KeyError:
            return "Invalid origin"
        try:
            destination = self.travel_info.airports[destination_code]
        except KeyError:
            return "Invalid destination"
        return self.calcFlightCost(origin, destination)

    def routeCost(self, airport_codes):
        """Calculate the cost of a route as given, with list of airport codes as argument. Return cost. """
        route = self.buildRoute(airport_codes)
        return self.calcRouteCost(route)

    def cheapestRoute(self, airport_codes):
        """ Calculate the cheapest route given a list of airport codes. Return Itinerary object. """
        route = self.buildRoute(airport_codes)
        if not route:   # If route could not be built because of errors in input.
            return None
        route_itin = Itinerary(route)
        return self.calcCheapestRoute(route_itin)

    def cheapestRoutesFromFile(self, file_routes, printout=True, fileout=False):
        """ Calculate the cheapest route, given a list of airport codes from a file. Routes include names. Return ([itineraries], [errors]). """
        # each route in file_routes has a name at index 0. 
        result_itins = []
        errors = []
        start_time = time.time()
        try:
            for f_route in file_routes: # Processes route inputs one at a time.
                name = f_route[0]
                route = self.buildRoute(f_route[1])
                if not route:   # Problem with input data. Route couldn't be built
                    errormsg = "Error building route:\t{name}: {route}".format(name=name, route=f_route[1])
                    errors.append(errormsg)
                    if printout: print(errormsg + "\n")
                    continue
                elif len(route.airports) != 5:  # Incorrect number of airports in route
                    errormsg = "Route contains {num} airports:\t{name}: {route}".format(num=len(route.airports), name=name, route=route.getSimpleString())
                    errors.append(errormsg)
                    if printout: print(errormsg + "\n")
                    continue
                route_itin = Itinerary(route, name)
                cheap_itin = self.calcCheapestRoute(route_itin)
                result_itins.append(cheap_itin)
                if printout: print(cheap_itin)
        except (KeyError, TypeError):   # Something is wrong with file_routes. This shouldn't happen in normal program use.
            errormsg = "Invalid file"
            errors.append(errormsg)
            if printout: print(errormsg + "\n")
            return result_itins, errors
        end_time = time.time()
        if printout: 
            print("Time taken: {time:.4f} seconds".format(time=end_time-start_time))
        if fileout:
            from inputoutput import FileHandler
            if FileHandler.writeItineraryOutput(fileout, result_itins):
                if printout: print("Output file {fileout} created successfully.".format(fileout=fileout))
            else:
                errormsg = "Output file {fileout} could not be created.".format(fileout=fileout)
                errors.append(errormsg)
                if printout: print(errormsg)
        return result_itins, errors

    def getCountryInfo(self, country_name):
        """Return a string containing info describing a country. """
        country = self.travel_info.getCountry(country_name)
        currency_info = country.currency.getInfo()
        num_airports = 0
        for airport in self.travel_info.airports.values():  # Count how many airports are in the country
            if airport.country.name == country_name:
                num_airports += 1
        return "Name: {country_name}\nNumber of Airports: {num_airports}\nCurrency:\t{currency_info}".format(**locals())
