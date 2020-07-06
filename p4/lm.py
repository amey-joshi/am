import numpy as np

def gradz_dot_dh(r, dh):
    gradz = [4 * r[0]**3 + r[1], r[0] + 4 * r[1]**3]

    return np.array([gradz[0] * dh[0], gradz[1] * dh[1]])
    
def hessian(r, lmbd):
    return (1 - lmbd) * 12 * r[0]**2 * r[1]**2 - 1

def euclidean_dist(r1, r2):
    return np.sqrt((r1[0] - r2[0])**2 + (r1[1] - r2[1])**2)

threshold = 0.00001
max_iter = 10000
step = [0.01, 0.01]

prev = [2, 1]
n = 0
lmbd = 2

while n < max_iter:
    n = n + 1
    hp = hessian(prev, lmbd)
    delta = gradz_dot_dh(prev, step)
    curr = prev + delta/hp
    if euclidean_dist(prev, curr) < threshold:
        print('Found an extremum.')
        break
    else:
        prev = curr

print(n)
print(curr)

