import math
import numpy as np
import matplotlib.pyplot as plt

def mu(x):
    y = np.ones(len(x))
    si = np.where(x < 0)[0]
    y[si] = 0

    return y

def beta3(x):
    b_0 = np.multiply(pow(x + 2, 3), mu(x + 2))/6
    b_1 = -2/3 * np.multiply(pow(x + 1, 3), mu(x + 1))
    b_2 = np.multiply(pow(x, 3), mu(x))
    b_3 = -2/3 * np.multiply(pow(x - 1, 3), mu(x - 1))
    b_4 = np.multiply(pow(x - 2, 3), mu(x - 2))/6

    return b_0 + b_1 + b_2 + b_3 + b_4

alpha = math.sqrt(3) - 2

def eta(x):
    sum = 0
    for k in range(-5, 6):
        sum = sum + math.pow(alpha, abs(k)) * beta3(x - k)

    return sum

x = np.linspace(-5, 5, 300)
y = eta(x)
plt.plot(x, y)
plt.show()

