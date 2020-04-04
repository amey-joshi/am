import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate

x = np.linspace(0, 5, 11)
x1 = np.linspace(0, 5, 21)

y = np.cos(2*x)
f = interpolate.interp1d(x, y, 'linear')
g = interpolate.interp1d(x, y, 'cubic')
y1 = f(x1)
y2 = g(x1)

plt.plot(x, y, 'o')
plt.plot(x1, f(x1), '-', label = 'linear')
plt.plot(x1, g(x1), '--', label = 'cubic')
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title('Two different functions interpolating same data')
plt.legend()
plt.show()
