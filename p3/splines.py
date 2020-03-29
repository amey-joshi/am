import numpy as np
import matplotlib.pyplot as plt

def mu(x):
  y = np.ones(len(x))
  # Select indices of x where x[i] < 0.
  si = np.where(x < 0)[0]
  y[si] = 0
  return y

lo = -2.5
hi = 2.5
n_samples = 1001

x = np.linspace(lo, hi, n_samples)

# Compute the two terms of \beta^0(x)
b_0 = mu(x + 1/2)
b_1 = mu(x - 1/2)

beta_0 = b_0 - b_1

# Computer the three terms of \beta^1(x)
b_0 = np.multiply((x+1), mu(x+1))
b_1 = np.multiply(x, mu(x))
b_2 = np.multiply((x-1), mu(x-1))

beta_1 = b_0 - 2*b_1 + b_2

# Compute the four terms of \beta^2(x)
b_0 = np.multiply(pow(x + 3/2, 2), mu(x + 3/2))/2
b_1 = -3 * np.multiply(pow(x + 1/2, 2), mu(x + 1/2))/2
b_2 = 3 * np.multiply(pow(x - 1/2, 2), mu(x - 1/2))/2
b_3 = -np.multiply(pow(x - 3/2, 2), mu(x - 3/2))/2

beta_2 = b_0 + b_1 + b_2 + b_3

# We will call the five terms of \beta^3(x) b_0, b_1, b_2, b_3.
b_0 = np.multiply(pow(x + 2, 3), mu(x + 2))/6
b_1 = -2/3 * np.multiply(pow(x + 1, 3), mu(x + 1))
b_2 = np.multiply(pow(x, 3), mu(x))
b_3 = -2/3 * np.multiply(pow(x - 1, 3), mu(x - 1))
b_4 = np.multiply(pow(x - 2, 3), mu(x - 2))/6

beta_3 = b_0 + b_1 + b_2 + b_3 + b_4

p = plt.plot(x, beta_0, label = r'$\beta^0(x)$')
p = plt.plot(x, beta_1, label = r'$\beta^1(x)$')
p = plt.plot(x, beta_2, label = r'$\beta^2(x)$')
p = plt.plot(x, beta_3, label = r'$\beta^3(x)$')
p = plt.xlabel('x')
p = plt.ylabel(r'$\beta^n(x)$')
plt.title('B-splines')
plt.legend()
plt.show()
print('Fig.3 A few B-splines')
