import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

x1 = np.linspace(-5, 5, 11)
y1 = x1

R = np.concatenate((np.linspace(-3, -1, 15), np.linspace(1, 3, 15)))
x = np.outer(R, R)
y = np.outer(R, R)
z_im = -np.divide(y, (np.multiply(x - 1, x - 1) - np.multiply(y, y)))
z_re = np.divide(np.multiply(x, x-1) + np.multiply(y, y), np.multiply(x-1, x-1) - np.multiply(y,y))

fig = plt.figure()
ax = plt.axes(projection = '3d')
ax.plot_surface(x, y, z_re, cmap = 'viridis', edgecolor = 'none')
plt.show()

