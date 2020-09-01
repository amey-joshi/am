#!/bin/python

from ortools.sat.python import cp_model

# A worker can do a task at a particular cost. The problem consists in 
# allocating all workers to a task they can do at the minimal cost. There is
# additional constraint, The workers are divided into two teams and each
# team can work on at most a certain number of tasks.

# This problem can be solved with an MIP solver but a CP-SAT solver is a
# better option because the decision variables are boolean.

model = cp_model.CpModel()

# The data for the problem described above can be represented as a bi-partite
# graph. The adjacency matrix for the graph is:
bg = [[90, 76, 75, 70],
      [35, 85, 55, 65],
      [125, 95, 90, 105],
      [45, 110, 95, 115],
      [60, 105, 80, 75],
      [45, 65, 110, 95]]
n_workers = len(bg) # The number of rows.
n_tasks   = len(bg[0]) # The number of columns.

# The team structure.
team1 = [0, 2, 4]
team2 = [1, 3, 5]
team_max = 2

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
    model.Add(sum(x[i][j] for j in range(n_tasks)) <= 1)
# A task is allocated to exactly one worker.
for j in range(n_tasks):
    model.Add(sum(x[i][j] for i in range(n_workers)) == 1)
# A team can have at most team_max tasks assigned to its members.
model.Add(sum(x[i][j] for i in team1 for j in range(n_tasks)) <= team_max)
model.Add(sum(x[i][j] for i in team2 for j in range(n_tasks)) <= team_max)

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

