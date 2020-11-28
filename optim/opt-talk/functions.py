#!/bin/python

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 5, 100)
y1 = np.power(x - 2, 2)
y2 = np.log(10*x + 1)

plt.plot(x, y1, label = r"$y = (x - 2)^2$" + " Convex")
plt.plot(x, y2, label = r"$y = \log(10x + 1)$" + " Concave")
plt.legend()
plt.title("Convex and concave functions")
plt.savefig("f1.png")
