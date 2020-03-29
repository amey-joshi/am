import numpy as np
import matplotlib.pyplot as plt

# We want to consider signals for n = -5, -4, ..., 4, 5.
# Note that we want to simulate negative indexes. We do
# so by translating an index to its array position. An
# index i of the signal translates to (i + EXTENT) in the
# array. Thus, the signal indexes -5, -4, ..., 4, 5 map to
# array indexes 0, 1, ..., 10.
EXTENT = 5

# The vectors b_1^0 and c_1^0.
b = np.zeros(2 * EXTENT + 1)
c = np.zeros(2 * EXTENT + 1)

# Initial values
b[0 + EXTENT] = 1
c[0 + EXTENT] = 1

def get_b1(k):
    i = k + 5 # index in the array
    return (k + 1) * c[i] + (1 - k) * c[i - 3]

def get_c1(k):
    i = k + 5
    return (k + 3/2) * b[i + 1] + (1/2 - k)*b[i]

# The vectors b_1^1 and c_1^1.
B = np.zeros(2 * EXTENT + 1)
C = np.zeros(2 * EXTENT + 1)
for k in range(-3, 3):
    B[k + EXTENT] = get_b1(k)
    C[k + EXTENT] = get_c1(k)

print(B)
print(C)
              
