#!/bin/python

from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver

# A person needs three nutrients. Let's assume they are vitamins A, B and C.
Nutrition = [2000, 300, 430]
# They can be supplied by four foods. The first number if the calories supplied
# by a food type. The remaining three numbers are the nutrients.
Foods = [['Trout', 600, 203, 92, 100],
         ['CB Sandwich', 350, 90, 84, 230],
         ['Burrito', 250, 270, 80, 512],
         ['Hamburger', 500, 500, 90, 210]]
# A person needs a certain minimum calories.
MinCalories = 2500

solver = Solver.CreateSolver('diet', 'CBC')
# The decision variables. How much quantity of each food typu should a person
# consume?
consumption = [None] * len(Foods)
for i in range(0, len(Foods)):
  consumption[i] = solver.IntVar(1, solver.infinity(), Foods[i][0])

# The objective function is to minimize the number of calories.
objf = solver.Objective()
for i in range(0, len(Foods)):
  objf.SetCoefficient(consumption[i], Foods[i][1])

objf.SetMinimization()

# Add constraints. Unlike the previous examples where we had our constraints
# given to us as inequalities, here we will have to build them from the given
# data.

# The constraint that the nutrient needs must be met.
for i in range(0, len(Nutrition)):
  cn = solver.Constraint(Nutrition[i], solver.infinity()) # This is the rhs.
  for j in range(0, len(Foods)): # We build the lhs.
    cn.SetCoefficient(consumption[j], Foods[j][i + 2]) 

# The calorie needs should be met.
cn = solver.Constraint(MinCalories, solver.infinity())
for i in range(0, len(Foods)):
  cn.SetCoefficient(consumption[i], Foods[i][1])

status = solver.Solve()
if status == Solver.OPTIMAL:
  calories = solver.Objective().Value()
  for i in range(0, len(Foods)):
    amt = round(consumption[i].solution_value(), 4)
    print(f'{Foods[i][0]}: {amt}.')

  print(f'Calories: {calories}.')
else:
  print('The solver could not find an optimum.')

del solver, consumption, Nutrition, Foods, objf, cn
