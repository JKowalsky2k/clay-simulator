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
    x = np.zeros(len(time)) #initialise x array 
    y = np.zeros(len(time)) #initialise y array 
    x[0],y[0] = 0,0 #initial position at t=0s, ie motion starts at (0,0) 
    x[1],y[1] = x[0] + vx0*(2*dt), y[0]+vy0*(2*dt) #calculating 2nd elements of x & y based on init velocity 
    i=1 
    while y[i]>=0: #loop continuous until y becomes <0, ie projectile hits ground 
        f = 0.5 * gamm * (h - y[i]) * dt #intermediate 'function'; used in calculating x & y vals below 
        x[i+1] = ((2*x[i]-x[i-1]) + (f * x[i-1])) / (1 + f) #numerical integration to find x[i+1]... 
        y[i+1] = ((2*y[i]-y[i-1]) + (f * y[i-1]) - g*(dt**2) ) / (1 + f) # ...& y[i+1] 
        i = i+1 #increment i for next iteration 
    x = x[0:i+1] #truncate x array 
    y = y[0:i+1] #truncate y array 
    return x, y, (dt*i), x[i] #return x, y, flight time, range of projectile 

def translateToPixel(self, vector) -> tuple:
    # v = pygame.math.Vector2(vector.x, Constants.SCREEN_HEIGHT - vector.y)
    return (int(vector[0]), int(500 - vector[1]))

x,y,duration,maxrange = traj_fr(math.pi/4, v0)

print(f"{gamm} = ")
print(f'{x[0] = }', f'{x[-1] = }')
print(f'{y[0] = }', f'{y[len(y)//2] = }')

plt.plot(x, y, color="b", label="with gamma") #quick plot of x vs y to check trajectory 
plt.xlabel('x') 
plt.ylabel('y')

gamm = 0
x,y,duration,maxrange = traj_fr(math.pi/4, v0) 

print(f"{gamm} = ")
print(f'{x[0] = }', f'{x[-1] = }')
print(f'{y[0] = }', f'{y[len(y)//2] = }')

plt.plot(x, y, color="r", label="no gamma")
plt.legend()


plt.show()
