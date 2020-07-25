/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 25, 2020 at 3:58:01 PM
 *********************************************/

 /*
 Knapsack problem is an example of an NP-hard problem. 
 
 We are given a knapsack with a certain capacity in terms of the weight it can
 carry. We are also given a set of items. Each item has a weight, a value and
 a quantity. The quantity is the number of items of that kind.
 
 The goal of the knapsack problem is to fill it with items that maximize its 
 value. The problem described here is slightly different. It is called the 
 multi-knapsack problem. Here an item is also associated with a certain number
 of resources. Taking an item results in a consumption of these resources. We 
 must maximize the value of the knapsack while still being controlled by the
 availability of the resources.
 */
 
 // The problem data.
 // 1. The number of items.
 int NItems = ...;
 // 2. The number of resources.
 int NResources = ...;
 
 // We do not name the items and resources. Instead we identify them with a 
 // positive integer.
 range items = 1..NItems;
 range resources = 1..NResources;
 
 // 3. The availability of resources.
 int Availability[resources] = ...;
 // 4. The value of items.
 int Value[items] = ...;
 // 5. How much of a resource r is used while taking an item i?
 int Use[resources][items] = ...;
 
 // The decision variable is the number of items put in the knapsack.
 dvar int+ Take[items];
 dexpr int totalValue = sum(i in items) Value[i] * Take[i];
 maximize(totalValue);
 
 subject to {
   forall (r in resources)
     ct: sum(i in items) Use[r][i] * Take[i] <= Availability[r];   
 } 
 
 execute {
   writeln("totalValue", totalValue);
 }
 