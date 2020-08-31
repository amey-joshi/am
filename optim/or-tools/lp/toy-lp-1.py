#!/bin/python

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('a_simple_program', 'GLOP')

x = solver.NumVar(0, solver.infinity(), 'x') # x >= 0
y = solver.NumVar(0, solver.infinity(), 'y') # y >= 0

# x + 2y <= 14
solver.Add(x + 2*y <= 14)

# 3x - y >= 0
solver.Add(3*x - y >= 0)

# x - y <= 2
solver.Add(x - y <= 2)

# The objective function f(x, y) = 3x + 4y
solver.Maximize(3*x + 4*y)

# Solve the problem
solver.Solve()
opt_value = solver.Objective().Value()

print('Solution:')
print('x = ', round(x.solution_value(), 4))
print('y = ', round(y.solution_value(), 4))
print('f(x, y) = ', round(opt_value, 4))


