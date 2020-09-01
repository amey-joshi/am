#!/bin/python

from ortools.graph import pywrapgraph

def main():
    # The network consists of edges (s, t) with capacity c and unit costs u.
    s = [ 0, 0,  1, 1,  1,  2, 2,  3, 4]
    t = [ 1, 2,  2, 3,  4,  3, 4,  4, 2]
    c = [15, 8, 20, 4, 10, 15, 4, 20, 5]
    u = [ 4, 4,  2, 2,  6,  1, 3,  2, 3]

    # Each node can be either a supply node or a demand node. A demand is
    # depicted by a negative supply.
    supplies = [20, 0, 0, -5, -15]

    solver = pywrapgraph.SimpleMinCostFlow()

    for i in range(len(s)):
        solver.AddArcWithCapacityAndUnitCost(s[i], t[i], c[i], u[i])

    for i in range(len(supplies)):
        solver.SetNodeSupply(i, supplies[i])

    status = solver.Solve()
    if status == solver.OPTIMAL:
        print(f'Min cost: {solver.OptimalCost()}')
        print()
        print('  Arc  Flow / Capacity  Cost')
        for i in range(solver.NumArcs()):
            cost = solver.Flow(i) * solver.UnitCost(i)
            print(f'{solver.Tail(i)} -> {solver.Head(i)} {solver.Flow(i)} / {solver.Capacity(i)}  {cost}')
    else:
        print('The solver could not find a min cost flow.')
        print(f'status = {solver.StatusName(status)}')

if __name__ == '__main__':
    main()
 
