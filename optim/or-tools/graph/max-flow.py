#!/bin/python

from ortools.graph import pywrapgraph

def main():
    # The problem data. A directed edge (u, v) has a capacity c.
    u = [0, 0, 0, 1, 1, 2, 2, 3, 3]
    v = [1, 2, 3, 2, 4, 3, 4, 2, 4]
    c = [20, 30, 10, 40, 30, 10, 20, 5, 20]

    assert len(u) == len(v)
    assert len(v) == len(c)

    max_flow = pywrapgraph.SimpleMaxFlow()
    for i in range(len(u)):
        max_flow.AddArcWithCapacity(u[i], v[i], c[i])

    # Solve the problem, find max flow between nodes 0 and 1.
    status = max_flow.Solve(0, 4)
    if status == max_flow.OPTIMAL:
        print(f'Max flow: {max_flow.OptimalFlow()}')
        print()
        print('  Arc  Flow / Capacity')
        for i in range(max_flow.NumArcs()):
            print(f'{max_flow.Tail(i)} -> {max_flow.Head(i)} {max_flow.Flow(i)} / {max_flow.Capacity(i)}')

        print(f'Source side min-cut: {max_flow.GetSourceSideMinCut()}')
        print(f'Sink side min-cut: {max_flow.GetSinkSideMinCut()}')
    else:
        print('Unable to compute max-flow.')

if __name__ == '__main__':
    main()

