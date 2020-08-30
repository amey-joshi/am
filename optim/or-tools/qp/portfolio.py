#!/bin/python

# Example from http://cvxopt.org/examples/book/portfolio.html.
# Refer to 'Convex Optimization' by Boyd and Vandenberghe

from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp, options
import numpy as np

# Number of assets
n = 4

# Variance covariance matrix
S = matrix([[0.04, 0.006, -0.004, 0],
               [0.006, 0.01, 0, 0],
               [-0.004, 0, 0.0025, 0],
               [0, 0, 0, 0.1]])
# Mean returns
pbar = matrix([0.12, 0.1, 0.07, 0.03])
G = matrix(-1.0 * np.eye(n))
h = matrix(0.0, (n, 1))
A = matrix(1.0, (1, n))
b = matrix(1.0)

mu = 1000

solution = qp(mu * S, -pbar, G, h, A, b)
print(solution)
print(solution['x'])
print(sum(solution['x']))

