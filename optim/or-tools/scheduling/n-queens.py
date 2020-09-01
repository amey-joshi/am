#!/bin/python

import sys
from ortools.sat.python import cp_model

def main(size):
    model = cp_model.CpModel()
    # The decision variables. This is an array of 'size' number of queens,
    # q1, q2, .... If qi = j then it means that a queen is located on the
    # j-th row of the i'th column.
    queens = [model.NewIntVar(0, size-1, f'q{i}') for i in range(size)]

    # No more than one queen can occupy a position. Therefore,
    model.AddAllDifferent(queens)

    # We now add the diagonal constraints.
    for i in range(size):
        d1 = [] # One diagonal.
        d2 = [] # Another diagonal.

        for j in range(size):
            # Decision variables for queens on ascending diagonal.
            q1 = model.NewIntVar(0, 2*size, f'd1_{i}')
            d1.append(q1)
            model.Add(q1 == queens[j] + j) # Recall, ascending diagonal

            # Decision variables for queens on descending diagonal.
            q2 = model.NewIntVar(-size, size, f'd1_{i}')
            d2.append(q2)
            model.Add(q2 == queens[j] - j) # Recall, descending diagonal

        model.AddAllDifferent(d1)
        model.AddAllDifferent(d2)

    solver = cp_model.CpSolver()
    solutionPrinter = SolutionPrinter(queens)
    status = solver.SearchForAllSolutions(model, solutionPrinter)
    print()
    print(f'Found {solutionPrinter.SolutionCount()} solutions.')

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

    def SolutionCount(self):
        return self._solnCount

if __name__ == '__main__':
    size = 8
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    main(size)

