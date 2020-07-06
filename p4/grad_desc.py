import numpy as np
import matplotlib.pyplot as plt

def gradz_dot_dh(r, dh):
    gradz = [2*r[0] + r[1], r[0] + 2*r[1]]

    return np.dot(gradz, dh)

def euclidean_dist(r1, r2):
    return np.sqrt((r1[0] - r2[0])**2 + (r1[1] - r2[1])**2)

threshold = 0.000001
max_iter = 10000
step = [0.01, 0.01]

prev = [0.1, 0.1]
n = 0
while n < max_iter:
    n = n + 1
    curr = prev - gradz_dot_dh(prev, step)
    if euclidean_dist(prev, curr) < threshold:
        print('Found extremum.')
        break
    else:
        prev = curr

print(n)
print(curr)
