import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 4, 5)
y = 2*x

x1 = np.linspace(0, 4, 25)
y1 = 2*x1 + np.sin(np.pi * (x1 - np.floor(x1)))
y2 = 2*x1 + np.log(1 + (x1 - np.floor(x1)))

plt.plot(x, y, marker = 'o')
plt.plot(x1, y1)
plt.plot(x1, y2)
plt.show()

