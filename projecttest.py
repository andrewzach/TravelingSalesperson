# DT265: Object Oriented Software Development 1
# Travelling Salesperson Project
# Author:     Andrew Zacharias
# Student #:  D14127051
# Date:       May 2015

from traveldb import TravelDB
from travelcalc import TravelAgent
from inputoutput import InputHandler
from traveltesting import Tester

# Runs automatic tests from the Tester class and prints results.

try:
    travel_db = TravelDB()
    agent = TravelAgent(travel_db)
    inpt = InputHandler(travel_db)
except Exception as e:
    print("Error initializing program.")
    print(e.__class__.__name__, ": ", e)
    print("Unable to run automatic tests.")
    print()
    print("Goodbye.")
else:
    print("----AUTOMATIC TESTS-----")
    print()
    test = Tester(travel_db, agent, inpt)
    all_results = test.runAllTests()
    for result in all_results:
        print("{testname:32.32s} Result: {result}\t{info}\n".format(testname=result[0], result=result[1], info=result[2]))