import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import math
import os

m = 1
g = 9.81
d = 0.01 # dampening

dt = 0.01
T_max = 120

N = int(T_max/dt)

t = np.linspace(0,T_max,N)

x0 = (0,0,0,0,0)

time_now = 0

Fs = np.zeros(N)
dws = np.zeros(N)
inputs = np.zeros((N,2))

def reference(ts):
    return np.array([math.sin(ts*2), 0, math.sin(ts*2), 0, 0])*math.cos(ts/3)

def int_quad_2d(x, ts, m=1, g=9.81, d=0.01):

    ref = reference(ts)
    f, dw = control_input(x, ref)

    dx0 = x[1]
    dx1 = -f * math.sin(x[4]) #- d*x[1]
    dx2 = x[3]
    dx3 = f/m * math.cos(x[4]) - g #- d*x[3]
    dx4 = dw

    return dx0, dx1, dx2, dx3, dx4

def control_input(state, ref):
    error = np.subtract(ref,state)
    w_des = - max(-math.pi/4,min(math.pi/4, 0.8*error[0]-0.8*state[1]))
    dw = (w_des-state[4]*1)
    F = m*g/math.cos(state[4]) + 2*error[2] - state[3]
    F = max(0,F)
    F = min(20, F)
    return F, dw

y = np.array(integrate.odeint(int_quad_2d, x0, t))


for i in range(0, np.shape(y)[0]):
    inputs[i] = control_input(y[i],reference(t[i]))

y = np.concatenate((y,inputs),axis=1)
y = np.transpose(y)

fig, axs = plt.subplots(4, 1)
axs[0].plot(t, y[0], t, y[2])
axs[0].set_xlabel('time')
axs[0].set_ylabel('x and z')
axs[0].grid(True)

axs[1].plot(t, y[1], t, y[3], t, y[4])
axs[1].set_xlabel('time')
axs[1].set_ylabel('dx and dz and w')
axs[1].grid(True)

axs[2].plot(t, Fs, t, dws)
axs[2].set_xlabel('time')
axs[2].set_ylabel('F and dw')
axs[2].grid(True)

axs[3].plot(y[0], y[2])
axs[3].set_xlabel('x')
axs[3].set_ylabel('z')
axs[3].grid(True)

fig.tight_layout()
plt.show()

np.save(os.path.dirname(os.path.realpath(__file__))+"/measurements_sim/meas_states",y)

