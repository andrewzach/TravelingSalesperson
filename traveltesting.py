# Author:     Andrew Zacharias
# Student #:  D14127051
# Date:       May 2015

import time
from inputoutput import FileHandler
from travelcalc import Route, Itinerary

class Tester:
    """ Helper class used to test functionality of Travelling Salesperson program """

    def __init__(self, travel_db, travel_agent, input_handler):
        self.travel_db = travel_db
        self.agent = travel_agent
        self.inpt = input_handler

    def runAllTests(self):
        """ Run all tests to ensure program is working correctly. Return results as a list of [name, result, message] for each test"""
        all_tests = (self.testAirportDistance, self.testFlightCost, self.testRouteCost, self.testRoutePermutations, self.testCheapestRoute, self.testCheapestRouteExtraStop, self.testCheapestRouteFile, self.testFileWithErrors, self.testInvalidInputFiles, self.testAirportSearch)
        all_results = []
        for test in all_tests:
            all_results.append(test())
        return all_results

    def testAirportDistance(self):
        """ Test the airport distance function. Return list of [name, result, message] """
        # Test the distance between JFK and Dublin
        # Epected result: 5104
        test_name = "Route Distance Test"
        test_result = "Fail"
        try:
            dub = self.travel_db.getAirport("DUB")
            jfk = self.travel_db.getAirport("JFK")
            distance = int(jfk.distanceFrom(dub))
            if distance == 5104:
                test_result = "Pass"
            test_message = "Distance between JFK and DUB = {distance} (5104 expected)".format(**locals())
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

    def testFlightCost(self):
        """ Test the flight cost function. Return list of [name, result, message] """
        # Test the cost of a flight from JFK to Dublin
        # Expected result: 4843
        test_name = "Flight Cost Test"
        test_result = "Fail"
        try:
            cost = int(self.agent.flightCost("JFK", "DUB"))
            if cost == 4843:
                test_result = "Pass"
            test_message = "Cost from JFK to DUB = {cost} (4843 expected)".format(**locals())
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

    def testRouteCost(self):
        """ Test the route cost function. Return list of [name, result, message] """
        test_name = "Route Cost Test"
        test_result = "Fail"
        test_route = ["YYZ", "DUB", "AAL", "FKQ", "SYD", "FKQ", "YYZ"]
        try:
            cost = int(self.agent.routeCost(test_route))
            if cost == 9515:
                test_result = "Pass"
            test_message = "Cost for 'YYZ  SYD  DUB  AAL  FKQ  YYZ' = {cost} (9515 expected)".format(**locals())
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

    def testRoutePermutations(self):
        """ Test the Itinerary's buildPermutations function. Return list of [name, result, message] """
        # Test the build permutations function. Each route should have 456 possible permutations.
        # Make sure function runs successfully and results in the correct number of permutations.
        test_name = "Route Permutations Test"
        test_result = "Fail"
        test_route = ["YYZ", "DUB", "AAL", "FKQ", "SYD"]
        try:
            itin = Itinerary(Route(test_route))
            itin.buildPermutations()
            num_perm = len(itin.permutations)
            if num_perm == 456:
                test_result = "Pass"
            test_message = "Calculated permutations for route: YYZ  SYD  DUB  AAL  FKQ. {num_perm} calculated (456 expected).".format(**locals())
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message
    

    def testCheapestRoute(self):
        """ Test the cheapest route calculations. Return list of [name, result, message] """
        # Test the cheapest route for the following:
        # ["DUB", "TXT", "BRE", "ZQN", "SYD"] = ["DUB", "BRE", "TXL", "SYD", "ZQN", "DUB"] = 32118
        test_name = "Cheapest Route Test"
        test_result = "Fail"
        try:
            cheapest_itin = self.agent.cheapestRoute(["DUB", "TXL", "BRE", "ZQN", "SYD"])
            route_expected = self.agent.buildRoute(["DUB", "BRE", "TXL", "SYD", "ZQN", "DUB"])
            route_exp_cost = 32118
            if cheapest_itin.cheapest_route == route_expected and cheapest_itin.cheapest_cost == route_exp_cost:
                test_result = "Pass"
            test_message = "Route: 'DUB  TXL  BRE  ZQN  SYD  DUB'\t Cheapest: '{route}'\tCost: {cost}".format(route=cheapest_itin.cheapest_route.getSimpleString(), cost=cheapest_itin.cheapest_cost)
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

    def testCheapestRouteExtraStop(self):
        """ Test the cheapest route calculations where expected result has extra stop. Return list of [name, result, message] """
        # Test the cheapest route for the following:
        # ["YYZ", "SYD", "DUB", "AAL", "FKQ"] = ["YYZ", "DUB", "AAL", "FKQ", "SYD", "FKQ", "YYZ"] = 9515
        test_name = "Cheapest Route Test (Extra Stop)"
        test_result = "Fail"
        try:
            cheapest_itin = self.agent.cheapestRoute(["YYZ", "SYD", "DUB", "AAL", "FKQ"])
            route_expected = self.agent.buildRoute(["YYZ", "DUB", "AAL", "FKQ", "SYD", "FKQ", "YYZ"])
            route_exp_cost = 9515
            if cheapest_itin.cheapest_route == route_expected and cheapest_itin.cheapest_cost == route_exp_cost:
                test_result = "Pass"
            test_message = "Route: 'YYZ  SYD  DUB  AAL  FKQ  YYZ'\t Cheapest: '{route}'\tCost: {cost}".format(route=cheapest_itin.cheapest_route.getSimpleString(), cost=cheapest_itin.cheapest_cost)
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

    def testCheapestRouteFile(self):
        """ Test the file input - cheapest route functionality. Return list of [name, result, message] """
        # Test the file input function. Uses sampleinput.csv file which contains 7 routes.
        # Sums all cheapest route costs together and compares them to expected total.
        test_name = "File Input - Cheapest Route"
        test_result = "Fail"
        try:
            test_file = "sampleinput.csv"
            test_output = "sampleoutput.csv"
            expected_total_cost = 124230
            file_routes = FileHandler.getRouteInputFile(test_file)
            if not file_routes:
                test_message = "Error reading routes from file. Make sure {file} still exists.".format(file=test_file)
            else:
                results, errors = self.agent.cheapestRoutesFromFile(file_routes, printout=False, fileout=test_output)
                if errors:
                    test_message = errors[0]
                elif len(results) != 7:
                    test_message = "Incorrect number of results"
                else:
                    total_cost = 0
                    for itin in results:
                        total_cost += itin.cheapest_cost
                    if total_cost == expected_total_cost:
                        test_result = "Pass"
                    test_message = "Calculated total cost of 7 routes: {total_cost} ({expected_total_cost} expected). Output file {test_output} successfully created.".format(**locals())
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

    def testFileWithErrors(self):
        """ Test the file input - cheapest route functionality with a file that contains errors. Return list of [name, result, message] """
        test_name = "Cheapest Route File w/ Errors"
        test_result = "Fail"
        try:
            test_file = "random50errors.csv"
            expected_errors = 5
            file_routes = FileHandler.getRouteInputFile(test_file)
            if not file_routes:
                test_message = "Error reading routes from file. Make sure {file} still exists.".format(file=test_file)
            else:
                results, errors = self.agent.cheapestRoutesFromFile(file_routes, printout=False, fileout=False)
                num_errors = len(errors)
                num_results = len(results)
                if num_errors == expected_errors:
                    test_result = "Pass"
                test_message = "Processed input file {test_file}. {num_results} routes calculated successfully. {num_errors} errors ({expected_errors} expected).".format(**locals())
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

    def testInvalidInputFiles(self):
        """ Test the file input - cheapest route function with invalid and non-existant filenames """
        # Testing filenames for files that don't exist and filenames with invalid characters.
        # Trying to calculate the cheapest routes with these files should only return errors and no results.
        test_name = "Invalid/Non-exist Filename Test"
        test_result = "Fail"
        try:
            invalid_name = "af\\4**!//?.pptx"
            non_existant_file = "thisfilenothere.csv"
            file_routes_inv = FileHandler.getRouteInputFile(invalid_name)
            file_routes_ne = FileHandler.getRouteInputFile(non_existant_file)
            results_inv, errors_inv = self.agent.cheapestRoutesFromFile(file_routes_inv, printout=False, fileout=False)
            results_ne, errors_ne = self.agent.cheapestRoutesFromFile(file_routes_ne, printout=False, fileout=False)
            if errors_inv[0] == "Invalid file" and errors_ne[0] == "Invalid file":
                test_result = "Pass"
                test_message = "Testing File Input for: {invalid_name} and {non_existant_file}: Invalid file error successful.".format(**locals())
            else:
                test_message = "Testing File Input for: {invalid_name} and {non_existant_file}: Error not raised properly.".format(**locals())
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

    def testAirportSearch(self):
        """ Test the airport search function. Return list of [name, result, message] """
        test_name = "Airport Search Test"
        test_result = "Fail"
        try:
            search_results = self.travel_db.searchAirports("t","e","s","t")
            num_results = len(search_results)
            if num_results == 123:
                test_result = "Pass"
            test_message = "Searching code: t, country: e, city: s, name: t. {num_results} results found. (123 expected)".format(**locals())
        except Exception as e:
            test_message = "Exception {e}".format(e=e)
        return test_name, test_result, test_message

class Benchmarker:
    """ Helper class that runs performance benchmarks for Travelling Salesperson program. """

    def __init__(self, travel_db, travel_agent):
        self.agent = travel_agent
        self.travel_db = travel_db

    def benchmarkCheapestRoutes(self):
        """ Benchmark file input - cheapest route function with 1000 itineraries. Print out total time taken. """
        # Used to monitor performance and optimize efficiency. Averages around 7 seconds for me.
        print("Benchmarking Cheapest Routes...")
        input_file = "random1000.csv"
        file_routes = FileHandler.getRouteInputFile(input_file)
        if not file_routes:
            print("Test file ", input_file, " not found. Cannot benchmark.")
            return
        start = time.time()
        self.agent.cheapestRoutesFromFile(file_routes, printout=False)
        end = time.time()
        duration = end - start
        print("Cheapest routes for 1000 itineraries calculated in: {duration:.3f} seconds".format(**locals()))
