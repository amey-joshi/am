#!/bin/python

from ortools.linear_solver import pywraplp

# We solve the following problem.
# Maximize x + 10y subjec to:
# x + 7y <= 17.5; x <= 3.5; x, y >= 0
# where x, y are integers.

solver = pywraplp.Solver.CreateSolver('basic-mip', 'CBC')

# Integer decision variables
x = solver.IntVar(0, solver.infinity(), 'x')
y = solver.IntVar(0, solver.infinity(), 'y')

# Add constraints
solver.Add(x + 7*y <= 17.5)
solver.Add(x <= 3.5)

# Set up the objective function
solver.Maximize(x + 10*y)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print(f'Max value: {solver.Objective().Value()}.')
    print(f'x = {x.solution_value()}')
    print(f'y = {y.solution_value()}')
else:
    print('The solver did not find an optimal solution.')

