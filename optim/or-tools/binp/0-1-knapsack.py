#!/bin/python

# A 0-1 knapsack problem consists in choosing a subset of items with maximal
# value subject the a constraint of weight.
#
# Suppose that there are N items i_1, ..., i_N, each with weight w_1, ..., w_N
# and value v_1, ..., v_N. The problem consists in choosing the items in such
# a way that a bag of capacity W can be filled such the value of the items is
# maximal.
#
# It is called a 0-1 knapsack problem because each item can either be chosen
# or not.

from ortools.algorithms import pywrapknapsack_solver
from ortools.algorithms.pywrapknapsack_solver import KnapsackSolver

# The problem data.
values = [
    360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
    78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
    87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
    312
]
weights = [[
    7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
    42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
    3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
]]
capacity = [850]

solver = KnapsackSolver(KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, '0-1 knapsack')

solver.Init(values, weights, capacity)
solution = solver.Solve()

selection = []
item_wt = []
total_weight = 0

print(f'Total value = {solution}')
for i in range(0, len(values)):
    if solver.BestSolutionContains(i):
        selection.append(i)
        item_wt.append(weights[0][i])
        total_weight += weights[0][i]

print(f'Total weight = {total_weight}')
print(f'Selection = {selection}')
print(f'Item weights = {item_wt}')

