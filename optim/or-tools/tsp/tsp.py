#!/bin/python

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = [
      [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
      [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
      [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
      [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
      [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
      [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
      [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
      [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
      [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
      [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
      [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
      [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
      [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
    ]  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    data['codes'] = {0: 'New York', 1: 'Los Angeles', 2: 'Chicago', \
    3: 'Minneapolis', 4: 'Denver', 5: 'Dallas', 6: 'Seattle', 7: 'Boston', \
    8: 'San Francisco', 9: 'St. Louis', 10: 'Houston', 11: 'Phoenix', \
    12: 'Salt Lake City'}

    return data

def city(mgr, curr, codes):
    """ Get's city from its index. """
    return codes[mgr.IndexToNode(curr)]

def build_route(mgr, routing, solution, codes):
    """ Prints the route. """
    print(f'Distance covered: {solution.ObjectiveValue()} miles.')
    curr = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    cities = [] 

    while not routing.IsEnd(curr):
        cities.append(city(mgr, curr, codes))
        prev = curr
        curr = solution.Value(routing.NextVar(curr))
        route_distance += routing.GetArcCostForVehicle(prev, curr, 0)

    cities.append(city(mgr, curr, codes))

    return {"route": cities, "distance": route_distance}

def print_route(results):
    cities = results["route"]
    route_distance = results["distance"]
    print('Route:')
    print(' -> '.join([c for c in cities]))
    print(f'Route distance: {route_distance} miles')
    
def main():
    data = create_data_model()

    # Routing index manager. The 'depot' is the place at which one starts
    # the trip and where one returns.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), \
              data['num_vehicles'], data['depot'])

    # Routing model.
    routing = pywrapcp.RoutingModel(manager)

    def get_dist(i, j):
        """ Returns distance between two nodes. """
        src = manager.IndexToNode(i) # the source.
        dst = manager.IndexToNode(j) # the destination.

        return data['distance_matrix'][src][dst]

    transit_callback_index = routing.RegisterTransitCallback(get_dist)

    # Tells the solver how to compute cost of an edge.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = \
        (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(params)

    if solution:
        results = build_route(manager, routing, solution, data['codes'])
        print_route(results)

if __name__ == '__main__':
    main()

