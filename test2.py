# -*- coding: utf-8 -*- 
import matplotlib.pyplot as plt 
import numpy as np 
import math 
import scipy.constants as const
g = const.g #gravitation constant 
dt = 1e-3 #integration time step (delta t) 
v0 = 40 #initial speed at t=0 
angle = math.pi / 4 #launch angle in radians 
time = np.arange(0,100, dt) #create time axis 
gamm = 0.005 #gamma (used to compute f, below) 
h = 100 #height (used to compute f, below)

def traj_fr(angle, v0): #function that computes trajectory for some launch angle & velocity 
    vx0 = math.cos(angle)*v0 #compute x components of starting velocity 
    vy0 = math.sin(angle)*v0 #compute y components of starting velocity 
    # x = np.zeros(len(time)) #initialise x array 
    # y = np.zeros(len(time)) #initialise y array
    x = [0]
    y = [0]
    # x[0],y[0] = 0,0 #initial position at t=0s, ie motion starts at (0,0) 
    x.append(x[-1] + vx0*(2*dt))
    y.append(y[-1] + vy0*(2*dt)) #calculating 2nd elements of x & y based on init velocity 
    while y[-1]>=0: #loop continuous until y becomes <0, ie projectile hits ground 
        f = 0.5 * gamm * (h - y[-1]) * dt #intermediate 'function'; used in calculating x & y vals below 
        x.append(((2*x[-1]-x[-2]) + (f * x[-2])) / (1 + f)) #numerical integration to find x[i+1]... 
        y.append(((2*y[-1]-y[-2]) + (f * y[-2]) - g*(dt**2) ) / (1 + f)) # ...& y[i+1] 
    return x, y, None, None

x,y,duration,maxrange = traj_fr(math.pi/4, v0)

print(f'{x[0] =}', f'{x[-1] =}')
print(f'{y[0] =}', f'{y[-1] =}')

plt.plot(x, y, color="b", label="with gamma") #quick plot of x vs y to check trajectory 
plt.xlabel('x') 
plt.ylabel('y')

gamm = 0
x,y,duration,maxrange = traj_fr(math.pi/4, v0) 
plt.plot(x, y, color="r", label="no gamma")
plt.legend()


plt.show()
