#!/bin/python

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('a_simple_program', 'GLOP')

x = solver.NumVar(0, solver.infinity(), 'x') # x >= 0
y = solver.NumVar(0, solver.infinity(), 'y') # y >= 0

# x + 2y <= 14
cn0 = solver.Constraint(-solver.infinity(), 14)
cn0.SetCoefficient(x, 1)
cn0.SetCoefficient(y, 2)

# 3x - y >= 0
cn1 = solver.Constraint(0, solver.infinity())
cn1.SetCoefficient(x, 3)
cn1.SetCoefficient(y, -1)

# x - y <= 2
cn2 = solver.Constraint(-solver.infinity(), 2)
cn2.SetCoefficient(x, 1)
cn2.SetCoefficient(y, -1)

# The objective function f(x, y) = 3x + 4y
objf = solver.Objective()
objf.SetCoefficient(x, 3)
objf.SetCoefficient(y, 4)
objf.SetMaximization()

# Solve the problem
solver.Solve()
opt_value = 3 * x.solution_value() + 4 * y.solution_value()

print('Solution:')
print('x = ', round(x.solution_value(), 4))
print('y = ', round(y.solution_value(), 4))
print('f(x, y) = ', round(opt_value, 4))


