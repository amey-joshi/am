/*********************************************
 * OPL 12.10.0.0 Model
 * Author: ameyjoshi
 * Creation Date: Jul 26, 2020 at 11:11:39 AM
 *********************************************/
using CP;

{string} MainSubjects       = ...;
{string} Labs               = ...;
{string} OtherSubjects      = ...;
{string} NonTeacherSubjects = ...;
{string} RemainingSubjects 	= Labs union OtherSubjects union NonTeacherSubjects;
{string} Years    					= ...;
{string} Days    					  = ...;
{int}    FirstPart          = ...;
{int}    SecondPart         = ...;

// Decision variables
dvar int fpclasses[Years][Days][FirstPart][MainSubjects] in 0..1;
//dvar int spclasses[Years][Days][SecondPart][RemainingSubjects] in 0..1;

subject to {        
   // At most one class of a subject everyday.
   forall(y in Years)
     forall(d in Days)
       forall(s in MainSubjects)
         sum(p in FirstPart) fpclasses[y][d][p][s] <= 1;
         
   // Subjects should not collide.
   forall(y in Years)
     forall(d in Days)
       forall(p in FirstPart)
         sum(s in MainSubjects) fpclasses[y][d][p][s] <= 1;
         
   // Teachers should not have to be in more than one class simultaneously.   
   forall(d in Days)
     forall(p in FirstPart)
       forall (s in MainSubjects)
         sum(y in Years) fpclasses[y][d][p][s] <= 1;
           
   // Five periods of each subject
   forall(y in Years)
     forall(s in MainSubjects)
       sum(d in Days) sum(p in FirstPart) fpclasses[y][d][p][s] >= 5;     
}

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
	
	writeln("Timetable for class 12.")
  for (var p in FirstPart) {
  	for (var d in Days) {
  		for (var s in MainSubjects) {
  			if (fpclasses["12"][d][p][s] == 1) write(s + " ");
   		}  			
   }
   writeln();
	}    			
}

