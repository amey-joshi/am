import numpy as np
import matplotlib.pyplot as plt

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
bf = np.abs(np.fft.fft(beta_3))
bf1 = np.fft.fftshift(bf)/np.max(bf)
plt.plot(x[44:84], bf1[44:84], label = r'$\tilde{\beta}^3$')
##plt.plot(x, beta_3, label = r'$\beta^3(x)$')
plt.title('Cubic spline and its Fourier transform')
plt.legend()
plt.show()
