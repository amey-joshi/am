#!/bin/python

from ortools.sat.python import cp_model

# A worker can do a task at a particular cost. The problem consists in 
# allocating all workers to a task they can do at the minimal cost. There is
# additional constraint, Each task has a size and a worker cannot be assigned
# more tasks if the sum of their size exceeds a certain limit.

# This problem can be solved with an MIP solver but a CP-SAT solver is a
# better option because the decision variables are boolean.

model = cp_model.CpModel()

# The data for the problem described above can be represented as a 
# bi-partite graph. The adjacency matrix for the graph is:
bg = [[90, 76, 75, 70, 50, 74, 12, 68],
      [35, 85, 55, 65, 48, 101, 70, 83],
      [125, 95, 90, 105, 59, 120, 36, 73],
      [45, 110, 95, 115, 104, 83, 37, 71],
      [60, 105, 80, 75, 59, 62, 93, 88],
      [45, 65, 110, 95, 47, 31, 81, 34],
      [38, 51, 107, 41, 69, 99, 115, 48],
      [47, 85, 57, 71, 92, 77, 109, 36],
      [39, 63, 97, 49, 118, 56, 92, 61],
      [47, 101, 71, 60, 88, 109, 52, 90]]
task_sizes = [10, 7, 3, 12, 15, 4, 11, 5]
total_size_max = 15

n_workers = len(bg) # The number of rows.
n_tasks   = len(bg[0]) # The number of columns.

# The decision variable x_{i,j} is true is worker i is assigned task j and 
# false otherwise. We now create the boolean decision variables.
x = [False] * n_workers 
for i in range(n_workers):
    t = [False] * n_tasks
    for j in range(n_tasks):
        t[j] = model.NewBoolVar(f'x[{i}, {j}]')
    x[i] = t

# Add the constraints.
# Each worker is assigned at most one task.
for i in range(n_workers):
    model.Add(sum(x[i][j] * task_sizes[j] for j in range(n_tasks)) <= total_size_max)
# A task is allocated to exactly one worker.
for j in range(n_tasks):
    model.Add(sum(x[i][j] for i in range(n_workers)) == 1)

# Build the objective function.
terms = []
for i in range(n_workers):
    for j in range(n_tasks):
        terms.append(bg[i][j] * x[i][j])
model.Minimize(sum(terms))

# Solve the problem,
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'Min cost: {solver.ObjectiveValue()}')
    print()
    for i in range(n_workers):
        for j in range(n_tasks):
            if solver.BooleanValue(x[i][j]):
                print(f'Worker {i} assigned to task {j} at cost {bg[i][j]}.')
else:
    print('The solver did not find a solution.')

