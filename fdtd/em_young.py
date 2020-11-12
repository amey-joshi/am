#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:29:03 2020

@author: ajoshi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches # Plot rectangles
import os
import time

# Physical parameters of the problem.
c = 3e8                 # The speed of light in vacuum.
kappa = 7e3             # The relative dielectric permittivity of the screen.
sigma = 0.1             # The conductivity of the screen.
epsilon_0 = 8.854e-12   # Permittivity of free space in SI units.

# Geometrical parameters of the problem. 
# The extent of the domain. **You can alter these parameters.**
xe = 100 # Width.
ye = 100 # Height.

# The central points in either directions.
yc = ye // 2 - 1
xc = xe // 2 - 1

# The location of the perfectly matching layer. 
# PML starts after these limits.
pml_dn = ye // 20           # starting vertical position after PML.
pml_up = ye - pml_dn - 1    # ending vertical position before PML.
pml_lf = xe // 20           # starting horizontal position after PML.
pml_rt = xe - pml_lf - 1    # ending horizontal position before PML.

# Slit geometry. **You can alter these parameters.**
slit_height = 2 # height of each slit (vertical measure).
slit_sep = 15 # separation between both slits (vertical measure).
screen_thinkness = 2 # thickness of the screen (horizontal measure).

# The field vectors.
Ez = np.zeros((ye, xe))     # z-component of E field.
Dz = np.zeros((ye, xe))     # z-component of D field.
Hx = np.zeros((ye, xe))     # x-component of H field.
Hy = np.zeros((ye, xe))     # y-component of H field.
int_Ez = np.zeros((ye, xe)) # Time integral of E_z field.
int_Hx = np.zeros((ye, xe)) # Time integral of H_x field.
int_Hy = np.zeros((ye, xe)) # Time integral of H_y field.

Ez_in = np.zeros(xe) # z component of the incident E field.
Hx_in = np.zeros(xe) # x component of the incident H field.

# Simulation parameters and data.
cell_size = 0.01 # Cell size in m
dt = cell_size / 2*c
# The dielectric profile.
dep_1 = np.ones((ye, xe))
dep_2 = np.zeros((ye, xe))
# The absorbing boundary conditions.
lob = [0, 0]
hib = [0, 0]

# **You can alter this parameter.**
t0 = 10 # Time for which the source is generated. 
# **You can alter this parameter.**
nsteps = 500  # Number of time steps. 

# Vectors used for PML.
defy_2 = np.ones(ye)
defy_3 = np.ones(ye)
def2y_1 = np.zeros(ye)
def2y_2 = np.ones(ye)
def2y_3 = np.ones(ye)

defx_2 = np.ones(xe)
defx_3 = np.ones(xe)
def2x_1 = np.zeros(xe)
def2x_2 = np.ones(xe)
def2x_3 = np.ones(xe)

# Dictionary to keep track of desired points for plotting.
plotting_points = []
for n in range(1, nsteps+1):
    plotting_points.append({'label': 'a', 'num_steps': n, 'Ez_data': None})
    
# Functions used in simulation.

def point_on_screen(i, j):
    return (((i > 0 and i < yc - slit_height/2 - slit_sep/2) or 
              (i > yc - slit_sep/2 + slit_height/2 and 
               i < yc + slit_sep/2 - slit_height/2) or 
              (i > yc + slit_height/2 + slit_sep/2 and 
               i < ye)) 
              and (j > xc - screen_thinkness/2 and 
                   j < xc + screen_thinkness/2))

def build_dielectric_profile():
  for j in range(pml_lf, pml_rt): # vertical range
      for i in range(pml_dn, pml_up): # horizontal range
          if point_on_screen(i, j): # If position is inside the dielectric                  
              dep_1[i, j] = 1 / (kappa + (sigma * dt / epsilon_0))
              dep_2[i, j] = (sigma * dt / epsilon_0)
            
def create_pml():
  for n in range(pml_dn + 1):    
      # auxp stands for auxiliary parameter, as defined in eqn (3.20) of 
      # Houle and Sullivan's book.
      auxp = ((pml_dn + 1 - n) / (pml_dn + 1)) ** 3
      auxp /= 3
      
      defy_2[n] = 1 / (1 + auxp)
      defy_2[ye - 1 - n] = 1 / (1 + auxp)
      defy_3[n] = (1 - auxp) / (1 + auxp)
      defy_3[ye - 1 - n] = (1 - auxp) / (1 + auxp)
      
      defx_2[n] = 1 / (1 + auxp)
      defx_2[xe - 1 - n] = 1 / (1 + auxp)
      defx_3[n] = (1 - auxp) / (1 + auxp)
      defx_3[xe - 1 - n] = (1 - auxp) / (1 + auxp)
      
      auxp = ((pml_dn + 0.5 - n) / (pml_dn + 1)) ** 3
      auxp /= 3
      
      def2y_1[n] = auxp
      def2y_1[ye - 2 - n] = auxp
      def2y_2[n] = 1 / (1 + auxp)
      def2y_2[ye - 2 - n] = 1 / (1 + auxp)
      def2y_3[n] = (1 - auxp) / (1 + auxp)
      def2y_3[ye - 2 - n] = (1 - auxp) / (1 + auxp)
      
      def2x_1[n] = auxp
      def2x_1[xe - 2 - n] = auxp
      def2x_2[n] = 1 / (1 + auxp)
      def2x_2[xe - 2 - n] = 1 / (1 + auxp)
      def2x_3[n] = (1 - auxp) / (1 + auxp)
      def2x_3[xe - 2 - n] = (1 - auxp) / (1 + auxp)

def compute_fields(t): 
  if t % 100 == 0:
      print('|', end = '')
  elif t % 10 == 0:
      print('.', end = '')
      
  for j in range(1, xe):
      Ez_in[j] = Ez_in[j] + 0.5 * (Hx_in[j - 1] - Hx_in[j])
              
  # Absorbing Boundary Conditions
  Ez_in[0] = lob.pop(0)
  lob.append(Ez_in[1])  
  Ez_in[xe - 1] = hib.pop(0)
  hib.append(Ez_in[xe - 2])
    
  for j in range(1, xe):
      for i in range(1, ye):
          Dz[i, j] = defy_3[i] * defx_3[j] * Dz[i, j] + \
                      defy_2[i] * defx_2[j] * 0.5 * \
                      (Hy[i, j] - Hy[i - 1, j] -
                      Hx[i, j] + Hx[i, j - 1])

  # Source of electromagnetic waves.
  Ez_in[1] = (np.sin(2*np.pi*t/(2*t0)))**2
  
  for i in range(pml_dn, pml_up + 1):
      Dz[i, pml_lf] = Dz[i, pml_lf] + 0.5 * Hx_in[pml_lf - 1]
      Dz[i, pml_rt] = Dz[i, pml_rt] - 0.5 * Hx_in[pml_rt]
      
  for j in range(0, xe):
      for i in range(0, ye):
          Ez[i, j] = dep_1[i, j] * (Dz[i, j] - int_Ez[i, j])
          int_Ez[i, j] = int_Ez[i, j] + dep_2[i, j] * Ez[i, j]
                  
  for j in range(0, xe - 1):
      Hx_in[j] = Hx_in[j] + 0.5 * (Ez_in[j] - Ez_in[j + 1])
      
  for j in range(0, xe - 1):
      for i in range(0, ye - 1):
          curl_e = Ez[i, j] - Ez[i, j + 1]
          int_Hx[i, j] = int_Hx[i, j] + curl_e
          Hx[i, j] = def2x_3[j] * Hx[i, j] + def2x_2[j] * \
                      (0.5 * curl_e + def2y_1[i] * int_Hx[i, j])
              
  for i in range(pml_dn, pml_up + 1):
      Hx[i, pml_lf - 1] = Hx[i, pml_lf - 1] + 0.5 * Ez_in[pml_lf]
      Hx[i, pml_rt] = Hx[i, pml_rt] - 0.5 * Ez_in[pml_rt]
      
  for j in range(0, xe):
      for i in range(0, ye - 1):
          curl_e = Ez[i, j] - Ez[i + 1, j]
          int_Hy[i, j] = int_Hy[i, j] + curl_e
          Hy[i, j] = def2y_3[i] * Hy[i, j] - def2y_2[i] * \
                      (0.5 * curl_e + def2x_1[j] * int_Hy[i, j])
  
  for j in range(pml_lf, pml_rt + 1):
      Hy[pml_dn - 1, j] = Hy[pml_dn - 1, j] - 0.5 * Ez_in[j]
      Hy[pml_up, j] = Hy[pml_up, j] + 0.5 * Ez_in[j]
      
  # Save data at certain points for later plotting
  for pp in plotting_points:
      if t == pp['num_steps']:
          pp['Ez_data'] = np.copy(Ez)
          
def create_rectangle(xy, width, height):
    clr = '#ffffff'
    return patches.Rectangle(xy, width, height, 
                             linewidth=1, edgecolor=clr, facecolor=clr)

def save_plots():       
    print('Saving images.')
    if not os.path.exists('figs'):
        os.makedirs('figs')    
        
    pwd = os.getcwd()
    os.chdir('figs') 
    
    xy1 = (xc - screen_thinkness/2, 0)
    xy2 = (xc - screen_thinkness/2, yc - slit_sep/2 + slit_height/2)
    xy3 = (xc - screen_thinkness/2, yc + slit_sep/2 + slit_height/2)
    
    for sp_no, pp in enumerate(plotting_points):  
        if sp_no % 100 == 0:
            print('|', end = '')
        elif sp_no % 10 == 0:
            print('.', end = '')
                                  
        r1 = create_rectangle(xy1, screen_thinkness, yc - slit_sep/2 - slit_height/2)
        r2 = create_rectangle(xy2, screen_thinkness, slit_sep - slit_height)
        r3 = create_rectangle(xy3, screen_thinkness, yc - slit_sep/2 - slit_height/2)
        
        ax = plt.figure().add_subplot(1, 1, 1)
        ax.add_patch(r1)
        ax.add_patch(r2)
        ax.add_patch(r3)
    
        plt.imshow(pp['Ez_data'], interpolation='bilinear', cmap='gist_heat')
        plt.savefig(f'figs_{str(sp_no + 1)}.png')
        plt.close()
        
    os.chdir(pwd)
        
def generate_avg_plot():
    left = int(ye * 0.2)
    right = int(ye * 0.8)
    x = [int(f) for f in np.linspace(left, right - 1, num = right - left)]           
    
    t1 = int(nsteps * 0.8)
    t2 = nsteps - 1
    y0 = int(xe * 0.75) # Horizontal position where the filed is to be measured
    
    average = 0
    for i in range(t1, t2):
        average += abs(plotting_points[i]['Ez_data'][left:right, y0])
    
    plt.plot(x, average/(t2 - t1))
    plt.savefig('avg_intensity.png')
    plt.close()
          
def main():    
    build_dielectric_profile()
    create_pml()
    
    print('Computing the fields...')
    t1 = time.time()
    for t in range(1, nsteps + 1):
      compute_fields(t)
      
    t2 = time.time()
    print()
    print(f'Simulation took {round(t2 - t1, 2)} s.')
    generate_avg_plot()
    
    print('Saving the plots...')
    t1 = time.time()           
    save_plots()  
    t2 = time.time()
    print()
    print(f'Saving images took {round(t2 - t1, 2)} s.')          
    
main()
