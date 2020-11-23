#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 09:47:47 2020

@author: ajoshi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import os

# Physical parameters of the problem.
c = 3e8                 # The speed of light in vacuum.
kappa = 1e4             # The relative dielectric permittivity of the screen.
sigma = 0.3             # The conductivity of the screen.
epsilon_0 = 8.854e-12   # Permittivity of free space in SI units.
    
# Geometrical parameters of the problem. 
# The extent of the domain. **You can alter these parameters.**
ye = 200 # Extent along y-axis,
xe = 200 # Extent along x-axis

# The central points in either directions.
yc = ye // 2 - 1
xc = xe // 2 - 1

# The location of the perfectly matching layer.
y_pml_0 = 10                # starting vertical position after PML.
y_pml_1 = ye - y_pml_0 - 1  # ending horizontal position before PML.
x_pml_0 = 10                # starting horizontal position after PML.
x_pml_1 = xe - x_pml_0 - 1  # ending horizontal position before PML.

# Slit geometry. **You can alter these parameters.**
slit_ht  = 8    # The height of each slit.
slit_sep = 20   # The separation between both slits.
slit_wt  = 8    # The width of the slit.

# The field vectors.
Ez = np.zeros((ye, xe)) # E field.
Dz = np.zeros((ye, xe)) # D field.
Hx = np.zeros((ye, xe)) # x-component of the H field.
Hy = np.zeros((ye, xe)) # x-component of the H field.
Ez_inc = np.zeros(xe)   # z-component of the incident E field.
Hx_inc = np.zeros(xe)   # x-component of the incident H field.

# Simulation parameters and data.
cell_size = 0.01 # Cell size in m
dt = cell_size / 2*c
# Dielectric factors are the coefficients of time integrals of E_z field.
def_1 = np.ones((ye, xe))   # First dielectric factor.
def_2 = np.zeros((ye, xe))  # Second dielectric factor.

lob = [0, 0]    # Boundary at the lower end.
hob = [0, 0]    # Boundary at the higher end.

t0 = 10       # Time for which the source is generated. **You can alter this parameter.**
nsteps = 500  # Number of time steps. **You can alter this parameter.**

# Time integrals of electromagnetic fields.
int_Ez = np.zeros((ye, xe))    # Time integral of E_z field.
int_Hx = np.zeros((ye, xe))    # Time integral of H_x field.
int_Hy = np.zeros((ye, xe))    # Time integral of H_y field.

# Vectors used for PML.
def_3x = np.ones(ye)    # Third dielectric factor in x-direction.
def_4x = np.ones(ye)    # Fourth dielectric factor in x-direction.
def_5x = np.zeros(ye)   # Fifth dielectric factor in x-direction.
def_6x = np.ones(ye)    # Sixth dielectric factor in x-direction.
def_7x = np.ones(ye)    # Seventh dielectric factor in x-direction.
def_3y = np.ones(xe)    # Third dielectric factor in y-direction.
def_4y = np.ones(xe)    # Third dielectric factor in y-direction.
def_5y = np.zeros(xe)   # Fifth dielectric factor in y-direction.
def_6y = np.ones(xe)    # Sixth dielectric factor in y-direction.
def_7y = np.ones(xe)    # Seventh dielectric factor in y-direction.  

# Dictionary to keep track of desired points for plotting.
plotting_points = []
for n in range(1,nsteps+1):
    plotting_points.append({'label': 'a', 'num_steps': n, 'field_data': None})
    
# Functions used in simulation.
def on_screen(i, j):
    return ((i > 0 and i < yc - slit_ht/2 - slit_sep/2) or 
            (i > yc - slit_sep/2 + slit_ht/2 and i < yc + slit_sep/2 - slit_ht/2) or 
            (i > yc + slit_ht/2+slit_sep/2 and i < ye)) and (j > xc-slit_wt/2 and j < xc+slit_wt/2)
    
def build_dielectric_profile():
  for j in range(x_pml_0, x_pml_1): 
      for i in range(y_pml_0, y_pml_1): 
          if on_screen(i, j):                   
              def_1[i, j] = 1 / (kappa + (sigma * dt / epsilon_0))
              def_2[i, j] = (sigma * dt / epsilon_0)
            
def create_pml():
  for n in range(y_pml_0 + 1):   
      xn = 0.33 * (y_pml_0 + 1 - n / (y_pml_0 + 1)) ** 3
      
      def_3x[n] = 1 / (1 + xn)
      def_3x[ye - 1 - n] = 1 / (1 + xn)
      def_4x[n] = (1 - xn) / (1 + xn)
      def_4x[ye - 1 - n] = (1 - xn) / (1 + xn)
      
      def_3y[n] = 1 / (1 + xn)
      def_3y[xe - 1 - n] = 1 / (1 + xn)
      def_4y[n] = (1 - xn) / (1 + xn)
      def_4y[xe - 1 - n] = (1 - xn) / (1 + xn)
      
      xn = 0.33 * ((y_pml_0 - n + 0.5) / (y_pml_0 + 1)) ** 3
      
      def_5x[n] = xn
      def_5x[ye - 2 - n] = xn
      def_6x[n] = 1 / (1 + xn)
      def_6x[ye - 2 - n] = 1 / (1 + xn)
      def_7x[n] = (1 - xn) / (1 + xn)
      def_7x[ye - 2 - n] = (1 - xn) / (1 + xn)
      
      def_5y[n] = xn
      def_5y[xe - 2 - n] = xn
      def_6y[n] = 1 / (1 + xn)
      def_6y[xe - 2 - n] = 1 / (1 + xn)
      def_7y[n] = (1 - xn) / (1 + xn)
      def_7y[xe - 2 - n] = (1 - xn) / (1 + xn)

def compute_fields(t):     
    if t%10 == 0:
        print('.', end='')
        
    for j in range(1, xe):
        Ez_inc[j] = Ez_inc[j] + 0.5 * (Hx_inc[j - 1] - Hx_inc[j])
              
    # Absorbing Boundary Conditions
    Ez_inc[0] = lob.pop(0)
    lob.append(Ez_inc[1])  
    Ez_inc[xe - 1] = hob.pop(0)
    hob.append(Ez_inc[xe - 2])
    
    for j in range(1, xe):
        for i in range(1, ye):
            Dz[i, j] = def_4x[i] * def_4y[j] * Dz[i, j] + \
                      def_3x[i] * def_3y[j] * 0.5 * \
                      (Hy[i, j] - Hy[i - 1, j] -
                      Hx[i, j] + Hx[i, j - 1])

    # Source of electromagnetic waves.
    Ez_inc[1] = (np.sin(2*np.pi*t/(2*t0)))**2
  
    for i in range(y_pml_0, y_pml_1 + 1):
        Dz[i, x_pml_0] = Dz[i, x_pml_0] + 0.5 * Hx_inc[x_pml_0 - 1]
        Dz[i, x_pml_1] = Dz[i, x_pml_1] - 0.5 * Hx_inc[x_pml_1]
      
    for j in range(0, xe):
        for i in range(0, ye):
            Ez[i, j] = def_1[i, j] * (Dz[i, j] - int_Ez[i, j])
            int_Ez[i, j] = int_Ez[i, j] + def_2[i, j] * Ez[i, j]
                  
    for j in range(0, xe - 1):
        Hx_inc[j] = Hx_inc[j] + 0.5 * (Ez_inc[j] - Ez_inc[j + 1])
      
    for j in range(0, xe - 1):
        for i in range(0, ye - 1):
            curl_e = Ez[i, j] - Ez[i, j + 1]
            int_Hx[i, j] = int_Hx[i, j] + curl_e
            Hx[i, j] = def_7y[j] * Hx[i, j] + def_6y[j] * \
                      (0.5 * curl_e + def_5x[i] * int_Hx[i, j])
              
    for i in range(y_pml_0, y_pml_1 + 1):
        Hx[i, x_pml_0 - 1] = Hx[i, x_pml_0 - 1] + 0.5 * Ez_inc[x_pml_0]
        Hx[i, x_pml_1] = Hx[i, x_pml_1] - 0.5 * Ez_inc[x_pml_1]
      
    for j in range(0, xe):
        for i in range(0, ye - 1):
            curl_e = Ez[i, j] - Ez[i + 1, j]
            int_Hy[i, j] = int_Hy[i, j] + curl_e
            Hy[i, j] = def_7x[i] * Hy[i, j] - def_6x[i] * \
                      (0.5 * curl_e + def_5y[j] * int_Hy[i, j])
  
    for j in range(x_pml_0, x_pml_1 + 1):
        Hy[y_pml_0 - 1, j] = Hy[y_pml_0 - 1, j] - 0.5 * Ez_inc[j]
        Hy[y_pml_1, j] = Hy[y_pml_1, j] + 0.5 * Ez_inc[j]
      
        # Save data at certain points for later plotting
    for pp in plotting_points:
        if t == pp['num_steps']:
            pp['field_data'] = np.copy(Ez)
          
def build_rectangle(anchor, width, height):
    return patches.Rectangle(anchor, width, height,
                             linewidth=1, edgecolor='#ffffff',
                             facecolor='#ffffff' )

def save_plots(plotting_points):
    plt.rcParams['font.size'] = 12
    plt.rcParams['grid.color'] = 'gray'
    plt.rcParams['grid.linestyle'] = 'dotted'

    # Plot the dielectric in white color
    anchor1 = (xc - slit_wt/2, 0)
    anchor2 = (xc - slit_wt/2, yc - slit_sep/2 + slit_ht/2)
    anchor3 = (xc - slit_wt/2, yc + slit_sep/2 + slit_ht/2)
    
    # Build rectangles.
    r1 = build_rectangle(anchor1, slit_wt, yc - slit_sep/2 - slit_ht/2)
    r2 = build_rectangle(anchor2, slit_wt, slit_sep - slit_ht)
    r3 = build_rectangle(anchor3, slit_wt, yc-slit_sep/2 - slit_ht/2)
    
    for sn, plotting_point in enumerate(plotting_points):
        if sn % 10 == 0:
            print('.', '')

        ax = plt.figure().add_subplot(1, 1, 1)
        ax.add_patch(r1)
        ax.add_patch(r2)
        ax.add_patch(r3)
    
        plt.imshow(plotting_point['field_data'], interpolation='bilinear', cmap='gist_heat')
        plt.savefig(f'figs_{str(sn+1)}.png')
        plt.close()
    
def generate_intensity_plot():
    """Generate average intensity plot."""
    left = 40 
    right = 160 
    x = [int(f) for f in np.linspace(left, right - 1, num = right - left)]
       
    average = 0
    t1 = nsteps - 100
    t2 = nsteps - 1
    y_measure = 150 
    
    for i in range(t1, t2):
        average += abs(plotting_points[i]['field_data'][left:right, y_measure])
       
    plt.plot(x, average/(t2 - t1))     

def main():
    build_dielectric_profile()
    create_pml()
    
    print('The simulation has started.')
    start_time = time.time()
    for t in range(1, nsteps + 1):
      compute_fields(t)
    end_time = time.time()
    print(f'Simulation took {end_time - start_time} s.')
    
    print('Starting to save images to make gif...')
    # filepaths
    if not os.path.exists('figs'):    
        os.makedirs('figs')    
        
    pwd = os.getcwd() 
    save_plots(plotting_points)
    os.chdir('figs')    
    os.chdir(pwd)
    generate_intensity_plot()
    
main()

