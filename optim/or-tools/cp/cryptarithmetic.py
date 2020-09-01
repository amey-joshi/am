#!/bin/python

from ortools.sat.python import cp_model

# Is there an assignment of digits to the letter such that the equation
# CP + IS + FUN = TRUE is true?

line = 'CP + IS + FUN = TRUE'
chars = set(c for c in line if c.isalpha())

base = 10 # We are looking at decimals
if len(chars) > base:
    print('No assignment is possible')
    exit(0)

model = cp_model.CpModel()

# Decision variables
c = model.NewIntVar(1, base - 1, 'C')
p = model.NewIntVar(0, base - 1, 'P')
i = model.NewIntVar(1, base - 1, 'I')
s = model.NewIntVar(0, base - 1, 'S')
f = model.NewIntVar(1, base - 1, 'F')
u = model.NewIntVar(0, base - 1, 'U')
n = model.NewIntVar(0, base - 1, 'N')
t = model.NewIntVar(1, base - 1, 'T')
r = model.NewIntVar(0, base - 1, 'R')
e = model.NewIntVar(0, base - 1, 'E')

allVars = [c, p, i, s, f, u, n, t, r, e]
# All letters need to be assigned a different number.
model.AddAllDifferent(allVars)

# Add the constraint in the line
model.Add(c * base + p + i * base + s + f * base * base + u * base +
              n == t * base * base * base + r * base * base + u * base + e)
solver = cp_model.CpSolver()

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._variables = variables
        self._solnCount = 0

    def on_solution_callback(self):
        self._solnCount += 1
        for v in self._variables:
            print(f'{v}={self.Value(v)}', end=' ')
        print()

    def solution_count(self):
        return self._solnCount

solutionPrinter = SolutionPrinter(allVars)
status = solver.SearchForAllSolutions(model, solutionPrinter)
print(f'status = {solver.StatusName(status)}')

