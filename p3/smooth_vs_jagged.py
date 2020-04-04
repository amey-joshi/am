import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 100)
y1 = np.cos(x)
y2 = np.cos(x) + np.random.normal(0, 1, 100) * 0.05

plt.plot(x, y1)
plt.plot(x, y2)
plt.show()

