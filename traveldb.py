# Author:     Andrew Zacharias
# Student #:  D14127051
# Date:       May 2015

import csv
from math import pi, acos, sin, cos
from travelcalc import Route

class Currency:

    def __init__(self, code, name, euro_rate):
        self.code = code
        self.name = name
        self.euro_rate = euro_rate

    def __str__(self):
        return self.code

    def getInfo(self):
        """ Return a string with detailed information on the currency. """
        euro_inv = 1/self.euro_rate
        return "Code: {code}\t Name: {name}\n1 {code} = {euros:.4f} EUR\n1 EUR = {euro_inv:.4f} {code}"\
        .format(code=self.code, name=self.name, euros=self.euro_rate, euro_inv=euro_inv)

    def toEuro(self):
        return self.euro_rate

class Country:
    """ Simple class that links Airports and Currencies. """
    def __init__(self, name, currency_code, currencies_dict):
        self.name = name
        self.currency = currencies_dict[currency_code]

    def __str__(self):
        return self.name

class Airport(object):

    def __init__(self, airport_code, name, country_name, city, latitude, longitude, countries_dict):
        self.code = airport_code
        self.country = countries_dict[country_name]
        self.city = city
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.distance_cache = {}

    def __str__(self):
        return "Name: {name:31.31s}\tLocation: {location:31.31s}\tCode: {code}\tLat: {latitude:7.3f}\tLong: {longitude:7.3f}"\
        .format(name=self.name, location=self.country.name + " - " + self.city, code=self.code, \
        latitude=self.latitude, longitude=self.longitude)

    def getStringGUI(self):
        """ Return a string formatted for the GUI output """
        return "Name: {name:25.25s}\tLoc: {location:25.25s}\tCode: {code}\tLat: {latitude:7.3f}\tLong: {longitude:7.3f}"\
        .format(name=self.name, location=self.country.name + " - " + self.city, code=self.code, \
        latitude=self.latitude, longitude=self.longitude)

    def distanceFrom(self, airport2):
        """ Calculates the distance from a second airport and returns it as a float """
        # This function utilizes a cache to speed up repeated distance calculations.
        # Any calculation already done is stored in the dictionary distance_cache. Any calc
        # not already in this dictionary is added to it.
        # Distance = arccos (sin φ1 sin φ2 cos(θ1 - θ2) + cos φ1 cos φ2) * radius_of_earth
        if self.code == airport2.code:
            distance = 0
        elif airport2.code in self.distance_cache:
            return self.distance_cache[airport2.code]
        else:
            radius_earth = 6373  # km
            θ1 = self.longitude * (2 * pi)/360
            θ2 = airport2.longitude * (2 * pi)/360
            ϕ1 = (90 - self.latitude) * (2 * pi)/360
            ϕ2 = (90 - airport2.latitude) * (2 * pi)/360
            distance = acos(sin(ϕ1)*sin(ϕ2)*cos(θ1-θ2) + cos(ϕ1)*cos(ϕ2)) * radius_earth
            self.distance_cache[airport2.code] = distance
        return distance

    def getCurrency(self):
        return self.country.currency()

class TravelDB:
    """ Database-like class that contains dictionaries of currencies, countries, and airports """

    currency_fn = "currencyrates.csv"
    country_fn = "countrycurrency.csv"
    airport_fn = "airport.csv"

    def __init__(self, currency_file = currency_fn, country_file = country_fn, airport_file = airport_fn):
        from inputoutput import FileHandler
        self.currencies = FileHandler.buildCurrencyDict(currency_file)
        self.countries = FileHandler.buildCountryDict(country_file, self.currencies)
        self.airports = FileHandler.buildAirportDict(airport_file, self.countries)

    def getAirport(self, airport_code):
        """ Return Airport object corresponding to airport_code. Return None if not found """
        try:
            return self.airports[airport_code.upper()]
        except KeyError:
            return None

    def getCountry(self, country_name):
        """ Return Country object corresponding to country_name. Return None if not found"""
        try:
            return self.countries[country_name]
        except KeyError:
            return None

    def getCurrency(self, currency_code):
        """ Return Currency object corresponding to currency_code. Return None if not found"""
        try:
            return self.currencies[currency_code.upper()]
        except KeyError:
            return None

    def randomRoute(self):
        """ Return a randomly generated route as a list of airport codes. """
        import random
        route = []
        for i in range(5):
            random_airport = random.choice(list(self.airports.keys()))
            while random_airport in route:                          # If already in route, select another airport
                random_airport = random.choice(list(self.airports.keys()))
            route.append(random_airport)
        return route

    def searchAirports(self, code=None, country_name=None, city=None, name=None):
        """ Return a list of Airport objects matching all search criteria specified. """
        # This search starts with a list of all airports and removes any that do not meet each criteria.
        # The search terms can appear in any part of the attribute being searched. e.g. "re" matches Ireland. 
        results_list = list(self.airports.values())
        if code:
            results_list = [apt for apt in results_list if code.lower() in apt.code.lower()]
        if name:
            results_list = [apt for apt in results_list if name.lower() in apt.name.lower()]
        if city:
            results_list = [apt for apt in results_list if city.lower() in apt.city.lower()]
        if country_name:
            results_list = [apt for apt in results_list if country_name.lower() in apt.country.name.lower()]
        if not results_list:        # If no values are found, return list with None
            results_list = [None]

        return results_list