/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 26, 2020 at 11:11:39 AM
 *********************************************/

/*
The free edition of IBM ILOG CPLEX Optimization Studio restricts the size of the
problem it can solve. We are required to limit the number of decision variables
and constraints to 1000. Our problem has 800 decision variables. The number of 
constraints vary depending on how we specify the problem. 

(1) In order to safely stay within these limits, I have split the day into two. 
The first part has periods 1, 2, 3, 4 and 5. The second one has periods 6, 7 and
8. This partition follows from the constraint that all labs must be in the 
afternoon.

(2) Subjects that can be covered in the first half are called the main subjects.
They are listed in the file 'Timetable.dat'. 

(3) Subjects that must be covered in the second half are called remaining 
subjects. They are the labs and the other subjects. It was found that expressing
the constraint of three consecutive period for a lab was not working for both
the classes together. If it worked for class 11 it failed for class 12. Therefore,
I have used the trick of consolidating the three periods in the second part as
a single block. This tremendously eases the solution.
	(a) The three labs form a natural block.
	(b) SUPW is required to be for 4 periods and Physical Education (PE) for two.
	    To accommodate this requirement, I created one three hour block for SUPW 
	    and another one SUPW (1 period) and PE (2 periods). I call the latter
	    block 'Comb' (for combined).
	    
(4) The blocks created in the previous point are resolved into periods while
printing the timetable. 

(5) This edition of IBM ILOG CPLEX Optimization Studio can be downloaded free of
charge from the URL https://www.ibm.com/in-en/products/ilog-cplex-optimization-studio 
after creating an IBM id.

*/ 

using CP;

{string} MainSubjects       = ...;
{string} Labs               = ...;
{string} OtherSubjects      = ...;
{string} RemainingSubjects 	= Labs union OtherSubjects;
{string} Years    					= ...;
{string} Days    					  = ...;
{int}    FirstPart          = ...;
{int}    SecondPart         = ...;

// Decision variables
dvar int fpclasses[Years][Days][FirstPart][MainSubjects] in 0..1;
dvar int spclasses[Years][Days][SecondPart][RemainingSubjects] in 0..1;

subject to {
/*-----------------------------------------------------------------------------
											Constraints for the first part.
-------------------------------------------------------------------------------*/
 // At most one class of a subject everyday.
  forall(y in Years)
    forall(d in Days)
     forall(s in MainSubjects)
       sum(p in FirstPart) fpclasses[y][d][p][s] <= 1;
         
 // More than one subject should not be scheduled in a period.
	forall(y in Years)
  	forall(d in Days)
      forall(p in FirstPart)
        sum(s in MainSubjects) fpclasses[y][d][p][s] <= 1;
         
	// Teachers should not have to be in more than one class simultaneously.   
  forall(d in Days)
    forall(p in FirstPart)
      forall (s in MainSubjects)
        sum(y in Years) fpclasses[y][d][p][s] <= 1;
           
  // Five periods of each subject.
  forall(y in Years)
    forall(s in MainSubjects)
      sum(d in Days) sum(p in FirstPart) fpclasses[y][d][p][s] >= 5;     

/*-----------------------------------------------------------------------------
											Constraints for the second part.
-------------------------------------------------------------------------------*/
  // More than one lab or other combination should not be scheduled in a block.
  forall(y in Years)
    forall(d in Days)
      forall(p in SecondPart)
        sum(s in RemainingSubjects) spclasses[y][d][p][s] <= 1;
         
  // Teachers should not have to be in more than one class simultaneously.   
  forall(d in Days)
    forall(p in SecondPart)
      forall(s in RemainingSubjects)
        sum(y in Years) spclasses[y][d][p][s] <= 1;       
         
	// One session for each lab.
  forall(y in Years)
    forall(s in RemainingSubjects)
      sum(d in Days) sum(p in SecondPart) spclasses[y][d][p][s] == 1;            
}

/*
We now have the solution ready. We print it in the form of a time-table.
*/
execute {
  writeln("Timetable for class 11.")
  for (var p in FirstPart) {
  	for (var d in Days) {
  		for (var s in MainSubjects) {
  			if (fpclasses["11"][d][p][s] == 1) write(s + " ");
   		}  			
   }
   writeln();
	}
  for (var p in SecondPart) {
  	for (var d in Days) {
  		for (var s in RemainingSubjects) {
  			if (spclasses["11"][d][p][s] == 1) {
  			  if (s == "Comb") {
  			    write("SUP ")
  			  } else {
  			    write(s + " ");
  			  }
  			}
   		}  			
   	}
   	writeln();
   	for (var d in Days) {
  		for (var s in RemainingSubjects) {
  			if (spclasses["11"][d][p][s] == 1) {
  			  if (s == "Comb") {
  			    write("PEd ")
  			  } else {
  			    write(s + " ");
  			  }
  			}
   		}  			
   	}
   	writeln();
   	for (var d in Days) {
  		for (var s in RemainingSubjects) {
  			if (spclasses["11"][d][p][s] == 1) {
  			  if (s == "Comb") {
  			    write("PEd ")
  			  } else {
  			    write(s + " ");
  			  }
  			}
   		}  			
   	}
   writeln();
	}    
	
	writeln("Timetable for class 12.")
  for (var p in FirstPart) {
  	for (var d in Days) {
  		for (var s in MainSubjects) {
  			if (fpclasses["12"][d][p][s] == 1) write(s + " ");
   		}  			
   }
   writeln();
	}  
	
  for (var p in SecondPart) {
  	for (var d in Days) {
  		for (var s in RemainingSubjects) {
  			if (spclasses["12"][d][p][s] == 1) {
  			  if (s == "Comb") {
  			    write("PEd ")
  			  } else {
  			    write(s + " ");
  			  }
  			}
   		}  			
   	}
   	writeln();
   	for (var d in Days) {
  		for (var s in RemainingSubjects) {
  			if (spclasses["12"][d][p][s] == 1) {
  			  if (s == "Comb") {
  			    write("PEd ")
  			  } else {
  			    write(s + " ");
  			  }
  			}
   		}  			
   	}
   	writeln();
   	for (var d in Days) {
  		for (var s in RemainingSubjects) {
  			if (spclasses["12"][d][p][s] == 1) {
  			  if (s == "Comb") {
  			    write("SUP ")
  			  } else {
  			    write(s + " ");
  			  }
  			}
   		}  			
   	}
   writeln();
	}   			
}

