from cmath import cos
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from scipy import constants

m= 0.145
A = np.pi*(0.0366*2)**2/4
C = 0.5
rho = 1.2
D = rho*C*A/2
g = constants.g

t = 0
dt = 0.001
x = [0]
y = [0]
v = 50
angle = 45
vx = v*np.cos(np.deg2rad(angle))
vy = v*np.sin(np.deg2rad(angle))

while y[-1] >= 0:
    # ax = -(D/m)*v*vx
    # ay = -g-(D/m)*v*vy
    ax = 0
    ay = -g
    vx += ax * dt
    vy += ay * dt
    v = np.sqrt(vx**2 + vy**2)

    x.append( x[-1]+vx*dt+0.5*ax*dt*dt )
    y.append( y[-1]+vy*dt+0.5*ay*dt*dt )

plt.plot(x, y)
plt.show()


# # Drag coefficient, projectile radius (m), area (m2) and mass (kg).
# c = 0.47
# r = 0.05
# A = np.pi * r**2
# m = 0.2
# # Air density (kg.m-3), acceleration due to gravity (m.s-2).
# rho_air = 1.28
# g = 9.81
# # For convenience, define  this constant.
# k = 0.5 * c * rho_air * A

# # Initial speed and launch angle (from the horizontal).
# v0 = 10
# phi0 = np.radians(45)

# def deriv(t, u):
#     x, xdot, z, zdot = u
#     speed = np.hypot(xdot, zdot)
#     xdotdot = -k/m * speed * xdot
#     zdotdot = -k/m * speed * zdot - g
#     return xdot, xdotdot, zdot, zdotdot

# # Initial conditions: x0, v0_x, z0, v0_z.
# u0 = 0, v0 * np.cos(phi0), 0., v0 * np.sin(phi0)
# # Integrate up to tf unless we hit the target sooner.
# t0, tf = 0, 50

# def hit_target(t, u):
#     # We've hit the target if the z-coordinate is 0.
#     return u[2]
# # Stop the integration when we hit the target.
# hit_target.terminal = True
# # We must be moving downwards (don't stop before we begin moving upwards!)
# hit_target.direction = -1

# def max_height(t, u):
#     # The maximum height is obtained when the z-velocity is zero.
#     return u[3]

# soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True,
#                  events=(hit_target, max_height))
# print(soln)
# print('Time to target = {:.2f} s'.format(soln.t_events[0][0]))
# print('Time to highest point = {:.2f} s'.format(soln.t_events[1][0]))

# # A fine grid of time points from 0 until impact time.
# t = np.linspace(0, soln.t_events[0][0], 100)

# # Retrieve the solution for the time grid and plot the trajectory.
# sol = soln.sol(t)
# x, z = sol[0], sol[2]
# print('Range to target, xmax = {:.2f} m'.format(x[-1]))
# print('Maximum height, zmax = {:.2f} m'.format(max(z)))
# plt.plot(x, z)
# plt.xlabel('x /m')
# plt.ylabel('z /m')
# plt.show()