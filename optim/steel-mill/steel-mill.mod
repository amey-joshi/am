/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 25, 2020 at 11:12:45 PM
 *********************************************/
 /*
 The problem is described at http://www.csplib.org/Problems/prob038/.
 
 */
using CP;

tuple Order {
  key int orderId;
  int weight; // Weight of the coil.
	int color;  // By which process is a coil manufactured?
};
 
{Order} orders = ...;
 
// A slab can be used to make coils of at most these many colors.
int maxColors = ...; 
// How many slabs can we use for this order.
int maxSlabs = ...; 
int slabs[1..maxSlabs] = ...;
 
// Auxillary variables.
int nOrders = card(orders); // How many orders do we have?
{int} allColors = union(o in orders) {o.color}; // Set of all colors.
int allWeights[i in 0..(nOrders - 1)] = item(orders, i).weight;
int maxSlabWt = max(i in 1..maxSlabs)slabs[i];
 
// Decision variables.
// 1. Which slab are we using to satisfy an order?
dvar int usedSlab[orders] in 1..maxSlabs;
// 2. How much of the slab are we consuming?
dvar int consumed[1..maxSlabs] in 0..maxSlabWt;
// 3. Total loss
dexpr int totalLoss = sum(i in 1..maxSlabs)(slabs[i] - consumed[i]);
 
minimize(totalLoss);
 
subject to {
  forall(s in 1..maxSlabs) consumed[s] <= slabs[s];
  // Assign orders to slabs.
   pack(consumed, usedSlab, allWeights);
  // Use a slab for at most 'maxColors' coils.
  forall (s in 1..maxSlabs) {    
    ct2:
    sum(c in allColors)(or(o in orders: o.color == c)(usedSlab[o] == s)) <= maxColors;
  }
}  

execute {
  var n = 1;
  var violated = 0;
  for(var o in orders) {
    if (slabs[usedSlab[o]] <= o.weight) {
      writeln("Order " + n + " consumed more slab than available");
      violated = 1;
    }
  }
  
  if (violated == 1) {
    writeln("A constraint has been violated.");
  } else {
    writeln("No constraint is violated.")
  }
}

 
 
 
