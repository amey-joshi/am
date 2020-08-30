#!/bin/python

from ortools.linear_solver import pywraplp

# 'Hello world' of linear programming. We are given a list of food items
# with their calorie content and nutrition content. We are also given the
# minimum nutrition needed per day. We are asked to design a diet that meets
# all nutritional needs and supplies at least a certain number of calories.

# There are three nutrients, vitamins A, B and C.
Nutrition = [2000, 300, 430]
# Every food has calorie and vitamin content data.
FoodData = [['Trout', 600, 203, 92, 100],
            ['CB Sandwich', 350, 90, 84, 230],
            ['Burrito', 250, 270, 80, 512],
            ['Hamburger', 500, 500, 90, 210]]
# Minimum consumption
MinimumCalories = 2500

solver= pywraplp.Solver.CreateSolver('diet', 'GLOP')

# Create decision variables.
consumption = [] # How much food should one consume?
objf = solver.Objective()
for i in range(0, len(FoodData)):
    dvar = solver.NumVar(0, solver.infinity(), FoodData[i][0])
    objf.SetCoefficient(dvar, FoodData[i][1])
    consumption.append(dvar)

objf.SetMinimization()

# Add constraints
constraints = []
# Meet nutrition needs.
for i in range(0, len(Nutrition)):
    cn = solver.Constraint(Nutrition[i], solver.infinity())
    for j in range(0, len(FoodData)):
        cn.SetCoefficient(consumption[j], FoodData[i][2 + i])

    constraints.append(cn)

# Eat all foods.
for i in range(0, len(FoodData)):
    cn = solver.Constraint(0, solver.infinity())
    cn.SetCoefficient(consumption[i], 1)
    constraints.append(cn)

# Minimal calories must be eaten.
for i in range(0, len(FoodData)):
    cn = solver.Constraint(MinimumCalories, solver.infinity())
    for j in range(0, len(FoodData)):
        cn.SetCoefficient(consumption[j], FoodData[i][1])

# Solve the problem
status = solver.Solve()

if status == solver.OPTIMAL:
    calories_consumed = 0
    for i in range(0, len(consumption)):
       calories_consumed += consumption[i].solution_value() * FoodData[i][1]

    print(f'Calories consumed = {calories_consumed}') 
    for i in range(0, len(consumption)):
        print(f'{FoodData[i][0]} = {consumption[i].solution_value()}')
else:
    print('Error: problem could not be solved.')

 
