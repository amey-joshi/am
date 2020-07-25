/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 24, 2020 at 11:51:38 PM
 *********************************************/

 /*
 This problem is part of the OPL IDE tutorials.
 
 A manufacturer has some products he wants to sell, and these products
 are manufactured with resources. The products can be made in either of 
 two ways. They can be made inside the factory, where production consumes 
 scarce resources and there is a cost per unit to manufacture the products, 
 or they can be ordered from outside the factory. In the latter case there 
 is no resource usage but there is a higher cost per unit to purchase the 
 products. There is a constraint that all customer demand for the products 
 must be satisfied, and the business goal is to minimize cost.

The problem is to determine how much of each product should be produced 
inside the company and how much outside, while minimizing the overall 
production cost, meeting the demand, and satisfying the resource constraints.
 */
 
 // The problem's data. These are the parameters of the problem.
 {string} Products = ...;
 {string} Resources = ...;
 
 // If a product were to be manufactured internally, it will consume certain
 // resources. This matrix tells how much resource a product needs.
 float Consumption[Products][Resources] = ...;
 // How much supply of resources we have?
 float Capacity[Resources] = ...;
 // How much demand does a product have? We must meed the demand.
 float Demand[Products] = ...;
 // How much does it cost to make a unit of a product internally?
 float InsideCost[Products] = ...;
 // How much does it cost to buy a unit of a product?
 float OutsideCost[Products] = ...;
 
 
 // We want to find out how much of demand should be met internally and
 // how much should it be procured from outside. Therefore, our decision
 // variables are:
 dvar float+ Inside[Products];  // float+ means a non-negative real number.
 dvar float+ Outside[Products];
 
 // The objective functions is:
 dexpr float cost = sum (p in Products) (InsideCost[p]*Inside[p] + OutsideCost[p]*Outside[p]);
 minimize(cost);
 
 // The constraints are:
 subject to {
	// We have the resources to manufacture.
	forall (r in Resources) 
		ctCapacity: sum(p in Products) Consumption[p][r] * Inside[p] <= Capacity[r];
		
	// We are meeting the demand for each product.
	forall (p in Products)
	  ctDemand: Inside[p] + Outside[p] >= Demand[p];
} 

// Run the model. Its solution will appear at the bottom of the Problem
// tab. The Problem tab is the one that appears on bottom-left of the screen.
 
tuple R {float i; float o;};
{R} Result = {<Inside[p], Outside[p]> | p in Products};

execute {
  writeln("Minimal cost = ", cost);
  writeln("Results = ", Result); 
}  

