import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def f(x):
    return 1/(1 + 25 * pow(x, 2))

def fp(x):
    return -50 * np.divide(x, np.power(1 + 25*x*x, 2))

def mu(x):
    y = np.ones(len(x))
    si = np.where(x < 0)[0]
    y[si] = 0

    return y

def beta2(x):
    b_0 = np.multiply(pow(x + 3/2, 2), mu(x + 3/2))/2
    b_1 = -3 * np.multiply(pow(x + 1/2, 2), mu(x + 1/2))/2
    b_2 = 3 * np.multiply(pow(x - 1/2, 2), mu(x - 1/2))/2
    b_3 = -np.multiply(pow(x - 3/2, 2), mu(x - 3/2))/2

    return b_0 + b_1 + b_2 + b_3

def beta3(x):
    b_0 = np.multiply(pow(x + 2, 3), mu(x + 2))/6
    b_1 = -2/3 * np.multiply(pow(x + 1, 3), mu(x + 1))
    b_2 = np.multiply(pow(x, 3), mu(x))
    b_3 = -2/3 * np.multiply(pow(x - 1, 3), mu(x - 1))
    b_4 = np.multiply(pow(x - 2, 3), mu(x - 2))/6

    return b_0 + b_1 + b_2 + b_3 + b_4

x = np.linspace(-1, 1, 101)
tck = interpolate.splrep(x, f(x))
yn = tck[1] # The spline representation
ynp = np.diff(yn) # First difference of the spline
xp = (x - np.linspace(-50, 50, 101) + 1/2)[1:]
beta2_xp = beta2(xp)
fprep = np.sum(np.multiply(ynp[2:102], beta2_xp))
fptru = fp(xp)


