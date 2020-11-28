#!/bin/python

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 25, 100)
y = np.sqrt(x) * np.cos(x) + x/3
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("A function with several extrema")
plt.savefig("many.png")
