#!/bin/python

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('Ex 1 from Mosek', 'GLOP')

# The decision variables
x = solver.NumVar(0, solver.infinity(), 'x')
y = solver.NumVar(0, solver.infinity(), 'y')
z = solver.NumVar(0, solver.infinity(), 'z')

# The constraint x + y + z = 1
cn1 = solver.Constraint(1, solver.infinity())
cn1.SetCoefficient(x, 1)
cn1.SetCoefficient(y, 1)
cn1.SetCoefficient(z, 1)

cn2 = solver.Constraint(-solver.infinity(), 1)
cn2.SetCoefficient(x, 1)
cn2.SetCoefficient(y, 1)
cn2.SetCoefficient(z, 1)

# The objective function x + 2y - z.
objf = solver.Objective()
objf.SetCoefficient(x, 1)
objf.SetCoefficient(y, 2)
objf.SetCoefficient(z, -1)
objf.SetMinimization()

# Solve the problem
status = solver.Solve()
if status == solver.OPTIMAL:
    optimal_value = x.solution_value() + 2*y.solution_value() - z.solution_value()
    print(f'Optimal value = {optimal_value}')
    print(f'x = {x.solution_value()}, y = {y.solution_value()}, z = {z.solution_value()}')
else:
    print('The solver failed to find an optimal value.')

