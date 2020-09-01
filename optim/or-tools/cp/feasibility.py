#!/bin/python

# Is there a feasible assignment to a constraint programming solution?

from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables
        self._solnCount = 0

    def on_solution_callback(self):
        self._solnCount += 1
        for v in self._variables:
            print(f'{v}={self.Value(v)}', end = ' ')
        print()

    def solution_count(self):
        return self._solnCount

model = cp_model.CpModel()

allowedVals = range(2)
x = model.NewIntVar(min(allowedVals), max(allowedVals), 'x')
y = model.NewIntVar(min(allowedVals), max(allowedVals), 'y')
z = model.NewIntVar(min(allowedVals), max(allowedVals), 'z')

model.Add(x != y)
model.Add(y != z)
model.Add(x + y + z <= 5)

solver = cp_model.CpSolver()
solutionPrinter = SolutionPrinter([x, y, z])
status = solver.SearchForAllSolutions(model, solutionPrinter)

print(f'Status = {solver.StatusName(status)}')
print(f'Found {solutionPrinter.solution_count()} solutions.')

