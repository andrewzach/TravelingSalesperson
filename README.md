# TravelingSalesperson
A school project completed for my Intro to Object Oriented Software Development class. A solution to a variant of the traveling salesperson problem.
Description of assignment is below:

## Problem Statement	   
 
The sales manager for your company wants a program that will streamline the sales teams travel plans. He describes the problem to you as follows: 
 
Each month, a salesperson needs to leave their home city and visit prospective customers in 4 other cities. These cities could be different each month. The sales manager wants to minimise the travel costs by choosing the most economic route between the cities for each sales person. 
#### Rules	   	   
- The first airport is the home airport and the other 4 are destinations.  
- Start and finish in first city. Visit each other city (at least) once 
- There must be 5 days between trips so 7 trips in total can be done in one month 
- Distance between airports calculated as great circle flight 
- Cost of leg calculated in local currency of city .
- The cost for a given leg of a journey is calculated as the exchange rate of origin city airport versus the destination city airport) multiplied by the distance 
- The best route is the cheapest option 

#### Tasks
- Create a program that will allow a user to choose 5 airports.
- The program needs to read a file with a list of sales people and airports and write a file with the best routes calculated per sales person
- A graphic user interface to allow a sales person to input their routes and display the cost 
