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

def traj_fr(angle, v0):
    vx0 = math.cos(angle)*v0
    vy0 = math.sin(angle)*v0
    x = [0]
    y = [0]
    x.append(x[-1] + vx0*(2*dt))
    y.append(y[-1] + vy0*(2*dt))
    while y[-1] >= 0:
        f = 0.5 * gamm * (h - y[-1]) * dt
        x.append(((2*x[-1]-x[-2]) + (f * x[-2])) / (1 + f))
        y.append(((2*y[-1]-y[-2]) + (f * y[-2]) - g*(dt**2) ) / (1 + f))
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
