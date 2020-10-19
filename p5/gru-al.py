import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import math
import random

# Helper functions
def get_random_weights(n):
    """Generate n random numbers whose total is 1."""
    R = random.sample(range(1, 11), n)
    return np.array([r/sum(R) for r in R])


def get_random_points(radius, n):
    """Generate n random points on a circle of given radius centred at the origin."""
    W = get_random_weights(n)
    points = [[radius*np.cos(2*np.pi*w), radius*np.sin(2*np.pi*w)] for w in W]
    
    return points

def list_mul_2d(M, m):
    """ M is a list of lists. Multiply each one of them by m."""
    return [[m * x for x in L] for L in M]

def eu_dist(x1, x2):
    """Euclidean distance between points x1 and x2 in R^n."""   
    return np.linalg.norm(x1 - x2)

def get_distance(x_init, xs):
    return [eu_dist(x_init, x) for x in xs]

Wh = np.array([get_random_weights(3)])
AWv = np.array([get_random_weights(2)])
# Initial points on a small circle of radius 0.01.
r = 0.01
N = 10
x_inits = [[r*np.cos(2*n*np.pi/N), r*np.sin(2*n*np.pi/N)] for n in range(1, N + 1)]

# Build 4 x 3 weight matrix
w1 = get_random_weights(4)
w2 = get_random_weights(4)
w3 = get_random_weights(4)
W = np.matrix([w1, w2, w3]).T

def f(h, t, U, extra = 0):  
    v = np.matmul(U, h)
    v0 = v[0]
    v1 = v[0]
    [x, y] = h
    
    xdot = 0.5*(np.tanh(v0) - x)
    ydot = 0.5*(np.tanh(v1) - y)
    
    return [xdot, ydot]

def get_HW(x, Wh):
    H = np.matrix([x, x, x]).T
    print(f'H = {H.shape}')
    print(f'Wh = {Wh.shape}')
    return np.matmul(H, Wh.T)

def get_Ml(x, Wh, AWv):
    hw = np.array(get_HW(x, Wh))
    print(f'hw = {hw.shape}')
    print(f'AWv = {AWv.shape}')
    X = np.concatenate((hw, AWv.T), axis=None)
    return np.tanh(X)

def get_a(W, Ml):
    args = np.exp([np.matrix(Ml) @ W[:, i] for i in range(W.shape[1])])   
    return args/np.sum(args)

def get_y(x, Wh, AWv, W):
    Ml = get_Ml(x, Wh, AWv)
    a = get_a(W, Ml)
    H = np.matrix([x, x, x])
    return H @ a.flatten()

def aluint(x_init, times, U):
    times = np.linspace(0, 2, 2000)  
    xs = odeint(f, x_init, times, args = (U, 0))  
    print(f'xs = {xs.shape}, Wh = {Wh.shape}, AWv = {AWv.shape}, W = {W.shape}')
    print(f'xs[0] = {xs[0, :].shape}')
    ys = [get_y(xs[i, :], Wh, AWv, W) for i in range(xs.shape[1])]
    
    return ys

def main():
    U = 3 * np.eye(2)
    times = np.linspace(0, 2, 2000)
    ys = aluint(x_inits[0], times, U)

if __name__ == '__main__':
    main()
