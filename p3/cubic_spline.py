import numpy as np
import matplotlib.pyplot as plt
import math

N = 128

def mu(x):
  y = np.ones(len(x))
  # Select indices of x where x[i] < 0.
  si = np.where(x < 0)[0]
  y[si] = 0
  return y

lo = -2.5
hi = 2.5
n_samples = N

x = np.linspace(lo, hi, n_samples)
# We will call the five terms of \beta^3(x) b_0, b_1, b_2, b_3.
b_0 = np.multiply(pow(x + 2, 3), mu(x + 2))/6
b_1 = -2/3 * np.multiply(pow(x + 1, 3), mu(x + 1))
b_2 = np.multiply(pow(x, 3), mu(x))
b_3 = -2/3 * np.multiply(pow(x - 1, 3), mu(x - 1))
b_4 = np.multiply(pow(x - 2, 3), mu(x - 2))/6

beta_3 = b_0 + b_1 + b_2 + b_3 + b_4
alpha = math.sqrt(3) - 2
K = -6.0*alpha/(1 - alpha*alpha)

truncate_at = 20
eta = np.zeros(len(x) - 2*truncate_at)

for i in range(0, len(eta)):
    sum = 0
    for j in range(-truncate_at, truncate_at):
        sum += pow(alpha, np.abs(j)) * beta_3[i - j]

    eta[i] = sum

eta = K * eta
plt.plot(x[truncate_at:(128-truncate_at)], eta)
plt.show()
