# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def f2(h, alpha = np.pi/3.8):
  [x, y] = h
  xdot = 0.5*(np.tanh(0.75*(x*np.cos(alpha)-y*np.sin(alpha))) - x)
  ydot = 0.5*(np.tanh(0.75*(x*np.sin(alpha)+y*np.cos(alpha))) - y)

  return [xdot, ydot]

# Create the grid in the domain [-1, 1] x [-1, 1].
lo, hi = -0.5, 0.5
X, Y = np.meshgrid(np.linspace(lo, hi, 21), np.linspace(lo, hi, 21))
u, v = np.zeros(X.shape), np.zeros(Y.shape)

for i in range(X.shape[0]):
  for j in range(X.shape[1]):
    xp = f2([X[i, j], Y[i, j]])
    u[i,j] = xp[0]
    v[i,j] = xp[1]
   
Q = plt.quiver(X, Y, u, v, color='r')
plt.title(r'$\alpha = \pi/6$')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.xlim([lo, hi])
plt.ylim([lo, hi])
x_inits = [[0.5, 0.5], [0.25, 0.5], [0, 0.5], [-0.25, 0.5], [-0.5, 0.5], \
          [-0.5, 0.25], [-0.5, 0], [-0.5, -0.25], [-0.5, -0.5], \
          [-0.25, -0.5], [0, -0.5], [0.25, -0.5], [0.5, -0.5], \
          [0.5, -0.25], [0.5, 0], [0.5, 0.25]]

for x_init in x_inits:  
  times = np.linspace(0, 50, 2000)  
  xs = odeint(f2, x_init, times)
  plt.plot(xs[:,0], xs[:,1], '-', color = 'black') # path
  plt.plot([xs[0,0]], [xs[0,1]], 'o', markersize = 2) # start
  plt.plot([xs[-1,0]], [xs[-1,1]], 's', markersize = 2) # end
