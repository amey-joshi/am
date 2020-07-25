/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 25, 2020 at 6:15:06 PM
 *********************************************/
/*
The blending problem is also a part of CPLEX's tutorials. It is a mixed integer
linear progamming problem. Some of its decision variables are integers while the
rest are floats.

The problem involving mixing some metals into an alloy. The metal may come from 
several sources: in pure form or from raw materials, scraps from previous mixes, 
or ingots. The alloy must contain a certain amount of the various metals, as 
expressed by a production constraint specifying lower and upper bounds for the 
quantity of each metal in the alloy. Each source also has a cost and the problem 
consists of blending the sources into the alloy while minimizing the cost and 
satisfying the production constraints. 
*/

// The problem's data.
// 1. The number of metals
int nMetals = ...;
// 2. The number of raw materials
int nRaw = ...;
// 3. The number of scrap inputs.
int nScrap = ...;
// 4. The number of ingots.
int nIngot = ...;

// We next create a few ranges.
range metals = 1..nMetals;
range raws = 1..nRaw;
range scraps = 1..nScrap;
range ingots = 1..nIngot;

// 5. Other inputs.
float costOfMetals[metals] = ...;
float costOfRaw[raws] = ...;
float costOfScrap[scraps] = ...;
float costOfIngots[ingots] = ...;

// The alloy is made by mixing the metals. There is a lower and an upper bound
// to the proportion of a metal in the alloy.
float lowerBound[metals] = ...;
float upperBound[metals] = ...;

// How much metal does a unit of raw material, scrap and ingot have?
float percentRaw[metals][raws] = ...;
float percentScrap[metals][scraps] = ...;
float percentIngot[metals][ingots] = ...;

// How much alloy do we need?
int amtOfAlloy = ...;

// The decision variable
dvar float proportion[m in metals] in lowerBound[m] * amtOfAlloy .. upperBound[m] * amtOfAlloy;
dvar float+ p[metals];
dvar float+ r[raws];
dvar float+ s[scraps];
dvar int+   t[ingots];

// The objective function
dexpr float totalCost = 
	sum(i in metals) costOfMetals[i] * p[i] + 
	sum(j in raws)   costOfRaw[j] * r[j] +
	sum(k in scraps) costOfScrap[k] * s[k] + 
	sum(l in ingots) costOfIngots[l] * t[l];
	
minimize(totalCost);
subject to {
  forall(i in metals)
		ct1: 
			proportion[i] == p[i] + 
			sum(j in raws) percentRaw[i][j] * r[j] +
			sum(k in scraps) percentScrap[i][k] * s[k] +
			sum(l in ingots) percentIngot[i][l] * t[l];
		ct2: sum(i in metals) proportion[i] == amtOfAlloy;  
}


	




