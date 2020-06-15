#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 18:30:05 2020

@author: ameyjoshi
"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
from scipy import stats


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

x = f - m # This is the "error" between the images.
C = np.array([[36, np.sum(x)], [np.sum(x), np.sum(x**2)]])/36
# print(f'C = {C}')

DELTA = 0.1
den_sigma_4 = np.zeros(len(x))
delta_sq = DELTA**2

for j in range(0, len(den_sigma_4)):
  a = 1 + x[j]**2
  den_sigma_4[j] = delta_sq/a

sigma_4_sq = np.min(den_sigma_4)/(1 + 2 * np.sqrt(2))
sigma_4 = np.sqrt(sigma_4_sq)
# print(f'\sigma_4 = {sigma_4}')

# This is our starting vector
mu_0 = np.array([0, 0])
cov = np.array([[sigma_4_sq, 0], [0, sigma_4_sq]])
mu_samples = []
N = 20 # number of samples

frozen = stats.multivariate_normal(mu_0, cov)
mu_samples = frozen.rvs(10)

random.seed(12111842)

exact_g = []
apprx_g = []
error_g = []

for i in range(len(mu_samples)):
  mu = mu_samples[i]
  g = np.zeros(2)
  for j in range(len(x)):
    # Recall that the data for the fixed image is in the array x
    X = np.array([1, x[j]]) 
    coeff = -2 * ((1 - mu[1]) * x[j] - mu[0])
    g = g + coeff * X

  exact_g.append(g)

for i in range(len(mu_samples)):
  mu = mu_samples[i]
  g = np.zeros(2)
  # Select a new set of pixels for computation of each approximate gradient
  S = random.sample(range(0, 36), N)
  for j in range(len(S)):
    # Recall that the data for the fixed image is in the array x
    X = np.array([1, x[j]]) 
    coeff = -2 * ((1 - mu[1]) * x[j] - mu[0])
    g = g + coeff * X

  apprx_g.append(g)

for i in range(len(mu_samples)):
  error_g.append(exact_g[i] - apprx_g[i])
  
trace_C = C[0, 0] + C[1, 1]

s = 0 
for i in range(len(exact_g)):
  g_n = exact_g[i]
  s = s + g_n[0]**2 + g_n[1]**2

sigma_1_sq = 1/(N * trace_C)
# print(f'sigma_1_sq = {sigma_1_sq}')

all_a = np.zeros(len(x))
sigma_1 = np.sqrt(sigma_1_sq)
coeff = 0.1 / sigma_1

for i in range(len(x)):
  a = (1 + 2 * np.sqrt(2)) * (1 + 3.64 * 1E3 * x[i]**4)
  all_a[i] = coeff/np.sqrt(a)

a_max = np.min(all_a)
# print(f'a_max = {a_max}')

s1 = 0
s2 = 0
for i in range(len(exact_g)):
  g = exact_g[i]
  h = apprx_g[i]

  s1 = s1 + (g[0]**2 + g[1]**2)
  s2 = s2 + (h[0]**2 + h[1]**2)

eta = s1/(s1 + s2)
a = a_max * eta
f_min = eta - 1

# print(f'eta = {eta}')
# print(f'a = {a}')
# print(f'f_min = {f_min}')

err_prod = np.zeros(len(error_g) - 1)
zeta = 0.1

for i in range(1, len(error_g)):
  e1 = error_g[i]
  e2 = error_g[i - 1]
  err_prod[i - 1] = np.dot(e1, e2)

# print(err_prod)

omega = zeta * np.std(err_prod)
print(f'omega = {omega}')

def our_sigmoid(x):
  # Recall that f_max = 1
  return f_min + (1 - f_min)/(1 - np.exp(-x/omega)/f_min)

def calc_t(prev_t, g_curr, g_prev):
  arg = prev_t + our_sigmoid(np.dot(g_curr, g_prev))
  if arg > 0:
    return arg
  else:
    return 0

# We re-initialize the image data
f = np.zeros(36)
f[14] = f[15] = f[20] = f[21] =  f[35] = 128
m = np.zeros(36)
m[7] = m[8] = m[13] = m[14] = m[28] = 128
# 'Difference' between fixed and moving images.
x = f - m

# Parameters of the algorithm
MAX_ITER = 500 # Maximum number of iterations.
n_iter = 0     # Current iteration.

# Temporary variables
g_prev = np.array([1, 1]) # previous gradient
mu_prev = np.zeros(2)     # previous parameters
prev_t = 0                # previous 'time'

def compute_q(s):
    x = np.sum(s)/len(s)
    y = np.sum(s**2)/len(s)
    
    return x + 2 * np.sqrt(np.abs(y - x**2))

def compute_P(s1, s2):
    q1 = compute_q(s1)
    q2 = compute_q(s2)
    
    p1 = 1/(q1 + 0.01)
    p2 = 1/(q2 + 0.01)
    
    return np.diag([p1, p2])

while n_iter < MAX_ITER:
  n_iter = n_iter + 1
  m = mu_prev[0] + mu_prev[1] * f
  
  # Select a new set of pixels for computation of each approximate gradient
  S = random.sample(range(0, 36), 15)
  g = np.zeros(2)
  
  s1 = 0
  s2 = 0
  for j in range(len(S)):
    # Recall that the data for the fixed image is in the array x
    X = np.array([1, x[j]]) 
    coeff = -2 * ((1 - mu[1]) * x[j] - mu[0])    
    g = g + coeff * X    
    
  s1 = np.zeros(len(S))
  s2 = np.zeros(len(S))
  for j in range(len(S)):
      s1[j] = 1 * g[0]
      s2[j] = x[j] * g[1]
  
  curr_t = calc_t(prev_t, g, g_prev)  
  gamma = a_max/(curr_t + 1) # Recall that A = 1, alpha = 1
  
  # Compute the pre-conditioner
  P = compute_P(s1, s2)

  mu_prev = mu_prev + gamma * np.dot(P, g)
  g_prev = g
  prev_t = curr_t
  
print(f'mu = {mu_prev}')