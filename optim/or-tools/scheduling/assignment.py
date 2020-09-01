#!/bin/python

from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, shifts, nDays, nShifts, nPeople, solutions):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._nDays = nDays
        self._nShifts = nShifts
        self._nPeople = nPeople
        self._solutions = set(solutions)
        self._solnCount = 0

    def on_solution_callback(self):
        if self._solnCount in self._solutions:
            print(f'Solution {self._solnCount}')

            for d in range(self._nDays):
                print(f'Day {d}')
                for p in range(self._nPeople):
                    assigned = False
                    for s in range(self._nShifts):
                        if self.Value(self._shifts[(d,s,p)]):
                            assigned = True
                            print(f'    Person {p} works shift {s}')
                    if not assigned:
                        print(f'    Person {p} does not work.')
            print()

        self._solnCount += 1

    def solnCount(self):
        return self._SolnCount

nPeople = 4
nShifts = 3
nDays   = 3

allPeople = range(nPeople)
allShifts = range(nShifts)
allDays   = range(nDays)

model = cp_model.CpModel()

# Create the decision variables.
shifts = {}
for d in allDays:
    for s in allShifts:
        for p in allPeople:
            shifts[(d, s, p)] = model.NewBoolVar(f'shift[({d},{s},{p})]')

# Add constraints.
# Each shift, every day should have exactly one person assigned to it.
for d in allDays:
    for s in allShifts:
        model.Add(sum(shifts[(d,s,p)] for p in allPeople) == 1)

# Each person works is assigned at most one shift every day
for p in allPeople:
    for d in allDays:
        model.Add(sum(shifts[(d,s,p)] for s in allShifts) <= 1)

minShifts = (nShifts * nDays) // nPeople
maxShifts = minShifts + ((nShifts * nDays) % nPeople)

for p in allPeople:
    nShiftsAssigned = 0
    for d in allDays:
        for s in allShifts:
            nShiftsAssigned += shifts[(d,s,p)]

    model.Add(nShiftsAssigned >= minShifts)
    model.Add(nShiftsAssigned <= maxShifts)

solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solnPrinter = SolutionPrinter(shifts, nDays, nShifts, nPeople, range(5))
solver.SearchForAllSolutions(model, solnPrinter)

