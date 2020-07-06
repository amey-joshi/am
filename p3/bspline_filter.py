import numpy as np
import matplotlib.pyplot as plt

def mu(x):
    y = np.ones(len(x))
    # Select indices of x such that x[i] < 0.
    si = np.where(x < 0)[0]
    y[si] = 0

    return y

lo = -2.5
hi = +2.5
n_samples = 101

x = np.linspace(lo, hi, n_samples)

def beta_0(x):
    b0 = mu(x + 1/2)
    b1 = mu(x - 1/2)

    return b0 - b1

def convolve_and_normalize(x, y):
    z = np.convolve(x, y)
    z = z/np.max(z)

    return z

def add_to_plot(y, m, n):
    l = len(y)
    x = np.linspace(0, l, l) - l//2

    left = l//4
    right = l - left

    plt.plot(x[left:right], y[left:right], label = rf'$\beta_{m}^{n}$'.format(m, n))


beta_0_1 = beta_0(x)
beta_1_1 = convolve_and_normalize(beta_0_1, beta_0_1)
beta_2_1 = convolve_and_normalize(beta_1_1, beta_0_1)
beta_3_1 = convolve_and_normalize(beta_2_1, beta_0_1)

def b_m_0(m):
    x = np.zeros(n_samples)
    left = n_samples//2 - m//2
    right = n_samples//2 + m//2

    if m % 2 == 1:
        right = right + 1

    for i in range(left, right):
        x[i] = 1

    return x

b_2_0 = b_m_0(2)
b_3_2 = np.convolve(np.convolve(np.convolve(b_2_0, b_2_0), b_2_0), beta_3_1)
b_3_2 = b_3_2/8

