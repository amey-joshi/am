// --------------------------------------------------------------------------
// Licensed Materials - Property of IBM
//
// 5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55
// Copyright IBM Corporation 1998, 2013. All Rights Reserved.
//
// Note to U.S. Government Users Restricted Rights:
// Use, duplication or disclosure restricted by GSA ADP Schedule
// Contract with IBM Corp.
// --------------------------------------------------------------------------

/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 27, 2020 at 10:39:25 PM
 *********************************************/
// This is just a heavily documented version of the solution already supplied
// by IBM ILOG CPLEX Optimization Studio.
//
// Three cities are suppliers of a set of goods. Seven cities are consumers of
// the goods. The supply exactly matches the demand. How to meet the demand in
// the cheapest way? For example, the city FRA can source bands from GARY at 30
// dollars, CLEV at 22 and PITT at 19. Naturally, it should source most from 
// PITT. But PITT supplies it at an even cheaper rate to three other cities. 
// Therefore, those cities should get most from it. It is quite apparent that
// even in this relatively simple case, the problem cannot be solved in the
// head.

{string} Cities = ...;
{string} Products = ...;
float Capacity = ...;

float Supply[Products][Cities] = ...;
float Demand[Products][Cities] = ...;

// The total demand exactly matches the total supply.
assert
  forall(p in Products)
    sum(o in Cities) Supply[p][o] == sum(d in Cities) Demand[p][d];

// What does it take to transport a product p from one city to another?
float Cost[Products][Cities][Cities] = ...;
// How much should we transport from one city to another to meet the demand
// in the cheapest way?
dvar float+ Trans[Products][Cities][Cities];

// City o is the origin and city d is the destination.
minimize
  sum(p in Products, o ,d in Cities) // o and d both are in Cities. 
    Cost[p][o][d] * Trans[p][o][d];
   
subject to {
  // We are transporting everything that is supplied.
  forall(p in Products, o in Cities)
    ctSupply:  
      sum(d in Cities) 
        Trans[p][o][d] == Supply[p][o];
  // We are delivering everything that is transported.
  forall(p in Products, d in Cities) 
    ctDemand:
      sum(o in Cities ) 
        Trans[p][o][d] == Demand[p][d];
  // We are not exceeding the capacity of any route.
   forall(o, d in Cities )
     ctCapacity:
       sum( p in Products ) 
         Trans[p][o][d] <= Capacity;
}  

execute DISPLAY {
  writeln("trans = ", Trans);
}

tuple solutionT {
	string Products;
	string City1;
	string City2;
	float Trans;	
};

{solutionT} solution = {<p, c1, c2, Trans[p][c1][c2]> | p in Products, c1 in Cities, c2 in Cities: Trans[p][c1][c2] != 0};

execute {
  for (var s in solution) {
    writeln(s);
  }
}