#!/bin/python

# Bin-packing problem involves using the minimal number of bins to carry a
# certain number of items.
#
# Suppose that we are given items of a certain weight. They should be 
# transported through wagons of a certain capacity. What is the least number
# of wagons that we should hire to carry all goods?

itemWts = [48, 30, 19, 36, 36, 27, 42, 42, 36, 24, 30]
maxwt = 100

# We ensure that every item can be fitted in a wagon. That is, none of them
# has a weight more than the wagon's capacity.

from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Solver

solver = Solver.CreateSolver('bin-packing', 'CBC')

# The decision variables are of the form x_{ij}. They take a value 1 if
# item i is put in wagon j, 0 otherwise.
nItems = len(itemWts)
nWagons = nItems

x = {}
for i in range(0, nItems):
    for j in range(0, nWagons):
        vname = f'x[{i}, {j}]'
        x[(i, j)] = solver.IntVar(0, 1, vname)

# Recall that we need at most as many wagons as we have items. w[i] is 1
# is wagon i is used.
w = [None] * nWagons
for i in range(0, nWagons):
    w[i] = solver.IntVar(0, 1, f'w[{i}]')

# We now add the constraints.
# Each item must be in exactly one bin.
for i in range(0, nItems):
    solver.Add(sum(x[(i, j)] for j in range(0, nWagons)) == 1)

# We cannot load a wagon beyond its capacity.
for j in range(0, nWagons):
    cn = sum(x[(i, j)]*itemWts[i] for i in range(0, nItems)) <= w[j]*maxwt
    solver.Add(cn)

# The objective function
solver.Minimize(solver.Sum([w[j] for j in range(0, nWagons)]))

status = solver.Solve()

if status == Solver.OPTIMAL:
    wagons_used = 0
    for j in range(0, nWagons):
        if w[j].solution_value() == 1:
            items = []
            loading = 0
            for i in range(0, nItems):
                if x[(i, j)].solution_value() != 0:
                    items.append(i)
                    loading += itemWts[i]

            if loading > 0:
                wagons_used += 1
                print(f'Wagon number {j}:')
                print(f'    Items: {items}')
                print(f'    Loading: {loading}')
                print()
    print()
    print(f'Number of wagons needed: {wagons_used}.')
else:
    print('The solver could not get an optimal solution.')


