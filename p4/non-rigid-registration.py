# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

f = np.zeros(36)
f[14] = f[15] = f[20] = f[21] =  f[35] = 128
ref = Image.new('1', (6, 6))
ref.putdata(f)

m = np.zeros(36)
m[7] = m[8] = m[13] = m[14] = m[28] = 128
tst = Image.new('1', (6, 6))
tst.putdata(m)

plt.figure()
plt.suptitle('Fixed and moving images')
p1 = plt.subplot(121)
p1.set_title('Fixed')
plt.imshow(ref)

p2 = plt.subplot(122)
p2.set_title('Moving')
plt.imshow(tst)

plt.show()

# Next cell
x = f - m # This is the "error" between the images.
C = np.array([[36, np.sum(x)], [np.sum(x), np.sum(x**2)]])/36

# Next cell
DELTA = 0.1
den_sigma_4 = np.zeros(len(x))
delta_sq = DELTA**2

for j in range(0, len(den_sigma_4)):
  a = 1 + x[j]**2
  den_sigma_4[j] = delta_sq/a

sigma_4_sq = np.min(den_sigma_4)/(1 + 2 * np.sqrt(2))
sigma_4 = np.sqrt(sigma_4_sq)

# Run the previous cells before running this one.
mu_0 = np.array([0.1, 0.1])
L = 5             # After how many iterations will we recompute the gradient.
K = 50           # Maximum number of times we will update the gradient.
x = f - m         # This is the "error" between the images.
n_samples = 6     # Number of samples to compute the stochastic gradient.

# Parameters mentioned in equation (5) of the paper.
theta_0 = 0.05
H_00 = theta_0 * np.eye(len(mu_0))
g_0 = np.ones(len(mu_0))

# We will keep the implementation simple by choosing the step size to be 1.

def compute_approx_g(x, S, mu):
  g = np.zeros(2)
  for j in range(len(x)):
    # Recall that the data for the fixed image is in the array x
    X = np.array([1, x[j]]) 
    coeff = -2 * ((1 - mu[1]) * x[j] - mu[0])
    g = g + coeff * X
    
  return g

import random

mu_prev = mu_0
H_prev = H_00
g_prev = g_0
m_prev = m

for k in range(K):
  g_sum = np.zeros(2) # The sum of gradients. We will use it for denoising.

  # Select a new set of pixels for computation of each approximate gradient
  S = random.sample(range(0, 36), n_samples)
  for l in range(L):
    mu_curr = mu_prev - np.dot(H_prev, g_prev)
    m_curr = m_prev * mu_curr[0] + mu_curr[1]
    x = m_curr - f
    
    g_curr = compute_approx_g(x, S, mu_curr)       
    s = mu_curr - mu_prev
    y = g_curr - g_prev

    rho = 1/np.dot(y, s)
    V = np.eye(len(mu_0)) - rho * np.outer(y, s)
    Vt = V.transpose()

    H_prev = np.dot(np.dot(Vt, H_prev), V) + rho * np.outer(s, s)
    g_sum = g_sum + g_prev
    g_prev = g_curr
    mu_prev = mu_curr

  avg_g = g_sum/L
  mu_curr = mu_prev - np.dot(H_prev, avg_g)
  m_curr = m_prev * mu_curr[0] + mu_curr[1]

  x = m_curr - f
  s = mu_curr - mu_prev
  y = avg_g - g_prev

  rho = 1/np.dot(y, s)
  V = np.eye(len(mu_0)) - rho * np.outer(y, s)
  Vt = V.transpose()

  H_prev = np.dot(np.dot(Vt, H_prev), V) + rho * np.outer(s, s)
  g_prev = avg_g
  mu_prev = mu_curr

print(f'Transformation parameters are mu = {mu_curr}')