#!/bin/python

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('Ex 1 from Mosek', 'GLOP')

# The decision variables
x = solver.NumVar(0, solver.infinity(), 'x')
y = solver.NumVar(0, solver.infinity(), 'y')
z = solver.NumVar(0, solver.infinity(), 'z')

# The constraint x + y + z = 1
solver.Add(x + y + z >= 1)
solver.Add(x + y + z <= 1)

# The objective function x + 2y - z.
solver.Minimize(x + 2*y - z)

# Solve the problem
status = solver.Solve()
if status == solver.OPTIMAL:
    optimal_value = solver.Objective().Value()
    print(f'Optimal value = {optimal_value}')
    print(f'x = {x.solution_value()}, y = {y.solution_value()}, z = {z.solution_value()}')
else:
    print('The solver failed to find an optimal value.')

