/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 25, 2020 at 10:40:08 PM
 *********************************************/
using CP;

/*
The documentation of the function is not very clear. Therefore, I am experimenting
with it to understand how it works. It appears that the function puts balls in 
bins and assigns a place to each one of them. It also keeps track of the number
of bins used.

Note that this is a constraints programming problem. We are not trying to 
maximize or minimize. We are only trying to find out if there is a solution that
satisfies all the constraints.
*/
int nBins = ...;
int nBalls = ...;
int weights[1..nBalls] = ...;
int capacity[1..nBins] = ...;

dvar int load[1..nBins];
dvar int place[1..nBalls] in 1..nBins;
dvar int nBinsUsed;

subject to {
  // A bin should not be loaded more than its capacity.
  forall(i in 1..nBins) load[i] <= capacity[i];
  // Every bin must be loaded.
  forall(i in 1..nBins) load[i] >= 1;
  // Pack the balls in the bins.
  pack(load, place, weights, nBinsUsed);
}

// Check that the pack function computes nBinsUsed correctly. It will always do.
assert nBinsUsed == nBins - count(load, 0);
// Check that the entire load of balls is places in the bins.
assert sum(i in 1..nBins) load[i] == sum(i in 1..nBalls) weights[i];

