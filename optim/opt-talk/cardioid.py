#!/bin/python

import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 2*np.pi, 1000)
a = 3
r = 3 + 3 * np.cos(theta)

plt.polar(theta, r)
plt.fill(theta, r)
plt.savefig('cardioid.png')
