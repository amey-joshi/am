#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 23:30:07 2020

@author: ameyjoshi
"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

f = np.zeros(36)
f[14] = f[15] = f[20] = f[21] =  f[35] = 128
ref = Image.new('1', (6, 6))
ref.putdata(f)

tst = ref.transform(ref.size, Image.AFFINE, (1, 0, 1, 0, 1, 1))
m = np.array(tst.getdata())

plt.figure()
plt.suptitle('Original and transformed images')
p1 = plt.subplot(121)
p1.set_title('Original')
plt.imshow(ref)

p2 = plt.subplot(122)
p2.set_title('Transformed')
plt.imshow(tst)

plt.show()

def mse(ref, tst):
    r = np.array(ref.getdata())
    t = np.array(tst.getdata())
    
    return np.pow(r - t, 2)

MAX_ITER = 200
mu_0 = np.ones(6) * 0.1

