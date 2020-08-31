#!/bin/python

# Knapsack problem is an example of an NP-hard problem. 
# 
# We are given a knapsack with a certain capacity in terms of the weight it can
# carry. We are also given a set of items. Each item has a weight, a value and
# a quantity. The quantity is the number of items of that kind.
 
# The goal of the knapsack problem is to fill it with items that maximize its 
# value. The problem described here is slightly different. It is called the 
# multi-knapsack problem. Here an item is also associated with a certain number
# of resources. Taking an item results in a consumption of these resources. We 
# must maximize the value of the knapsack while still being controlled by the
# availability of the resources.

from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver

# The data.
nResources = 7
nItems = 12
resourceAvailability = [18209, 7692, 1333, 924, 26638, 61188, 13360]
itemValue = [96, 76, 56, 11, 86, 10, 66, 86, 83, 12, 9, 81]
resourceUse = [
      [19,   1,  10,  1,   1,  14, 152, 11,  1,   1, 1, 1],
      [ 0,   4,  53,  0,   0,  80,   0,  4,  5,   0, 0, 0],
      [ 4, 660,   3,  0,  30,   0,   3,  0,  4,  90, 0, 0],
      [ 7,   0,  18,  6, 770, 330,   7,  0,  0,   6, 0, 0],
      [ 0,  20,   0,  4,  52,   3,   0,  0,  0,   5, 4, 0],
      [ 0,   0,  40, 70,   4,  63,   0,  0, 60,   0, 4, 0],
      [ 0,  32,   0,  0,   0,   5,   0,  3,  0, 660, 0, 9]]

solver = Solver.CreateSolver('multi-knapsack', 'CBC')

# How many numbers of each items should be packed? Each one of these is a 
# decision variable.
take = [None] * nItems
for i in range(0, nItems):
    take[i] = solver.IntVar(0, solver.infinity(), f'take[{i}]')

# Build the objective function.
objf = solver.Objective()
for i in range(0, nItems):
    objf.SetCoefficient(take[i], itemValue[i])

objf.SetMaximization()

for i in range(0, nResources):
    cn = solver.Constraint(0, resourceAvailability[i])
    for j in range(0, nItems):
        cn.SetCoefficient(take[j], resourceUse[i][j])

status = solver.Solve()
if status == Solver.OPTIMAL:
    maxval = solver.Objective().Value()
    for i in range(0, nItems):
        amt = take[i].solution_value()
        print(f'Item {i}: {amt}', end = ' ')

    print()
    print(f'Max value = {maxval}')
else:
    print('The solution could not be found')

