#!/bin/python

from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()

# Decision variables
ub = max([50, 45, 37])
x = model.NewIntVar(0, ub, 'x')
y = model.NewIntVar(0, ub, 'y')
z = model.NewIntVar(0, ub, 'z')

model.Add(2*x + 7*y + 3*z <= 50)
model.Add(3*x - 5*y + 7*z <= 45)
model.Add(5*x + 2*y - 6*z <= 37)

model.Maximize(2*x + 2*y + 3*z)

status = solver.Solve(model)
if status == cp_model.OPTIMAL:
    print(f'Objective function: {solver.ObjectiveValue()}')
    print('Assignment:', end = ' ')
    print(f'x={solver.Value(x)}, y={solver.Value(y)}, z={solver.Value(z)}')
else:
    print('Optimal solution could not be found.')

