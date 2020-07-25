/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 25, 2020 at 1:40:23 PM
 *********************************************/

 /*
 The diet problem is the 'hello world' of optimization. To make it relevant
 to the modern times we seek to minimize the calories while still ensuring
 that our food supplies the nutrients needed to be healthy.
 */
 
 // The data is:
 // 1. The list of foods.
 {string} Foods = ...;
 // 2. The nutrients.
 {string} Nutrients = ...;
 // 3. Calories in food.
 float Calories[Foods] = ...;
 // 4. Nutrient content.
 float Nutrition[Foods][Nutrients] = ...;
 // 5. Your needs.
 float Needs[Nutrients] = ...;
 
 // The decision variable is:
 dvar int+ consumption[Foods];
 
 // The objective function is:
 minimize (
 	sum(f in Foods) consumption[f] * Calories[f]
 );
 
 // The constraints are
 subject to {
   // You get the minimal nutrients you need.
   forall (n in Nutrients)
     ctNeeds: sum(f in Foods) consumption[f] * Nutrition[f][n] >= Needs[n];
     
   // Eat all foods, if you add this constraint you will end up eating
   // 700 calories more.
   // forall (f in Foods) consumption[f] >= 1;
 }

float calories = sum(f in Foods) consumption[f] * Calories[f];

execute {  
 writeln("Calories = ", calories);
} 
 
    
 
 