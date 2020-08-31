#!/bin/python 

from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver

def create_data_model():
  """Stores the data for the problem."""
  data = {}
  data['constraint_coeffs'] = [
      [5, 7, 9, 2, 1],
      [18, 4, -9, 10, 12],
      [4, 7, 3, 8, 5],
      [5, 13, 16, 3, -7],
  ]
  data['bounds'] = [250, 285, 211, 315]
  data['obj_coeffs'] = [7, 8, 2, 9, 6]
  data['num_vars'] = 5
  data['num_constraints'] = 4

  return data

data = create_data_model()

solver = Solver.CreateSolver('mip', 'CBC')
# Quite like in the case of the 'Diet problem' the decision variables are 
# created as elements of a list.
x = [None] * data['num_vars']
for i in range(0, len(x)):
  x[i] = solver.IntVar(0, solver.infinity(), f'x[{i}]')

print(f'Number of variables = {solver.NumVariables()}')

# Build the constraints.
for i in range(0, data['num_constraints']):
  cn = solver.Constraint(0, data['bounds'][i], f'cn[{i}]')
  for j in range(0, data['num_vars']):
    cn.SetCoefficient(x[j], data['constraint_coeffs'][i][j])
print(f'Number of constraints = {solver.NumConstraints()}')

# Build the objective function.
objf = solver.Objective()
for i in range(0, data['num_vars']):
  objf.SetCoefficient(x[i], data['obj_coeffs'][i])

objf.SetMaximization()

status = solver.Solve()
if status == Solver.OPTIMAL:
  maxval = solver.Objective().Value()
  for i in range(0, data['num_vars']):
    xv = round(x[i].solution_value(), 4)
    print(f'x[{i}]: {xv}', end=' ')

  print()
  print(f'maxval: {maxval}.')

  print('Problem solved in %f milliseconds' % solver.wall_time())
  print('Problem solved in %d iterations' % solver.iterations())
  print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
else:
  print('The solver could not find an optimum.')
  print(f'status = {status}')