#ballistic reentry in python, assuming lift is zero
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I

ha = np.linspace(0,122000,100000)#100km
Re = 6378000
Ve = 7500.0
beta = 0.1354/1000.0#density constant
rhos = 1.225
m = 1350.0
CD = 1.5
S = 2.8
gammae = -2.0*np.pi/180.0
Va = Ve*np.exp((1.0/(2*beta))*(rhos/(np.sin(gammae)))*(S*CD/m)*np.exp(-beta*ha))
drdt = Va*np.sin(gammae)
dhdt = drdt
dVdh = (Va[0:-2]-Va[1:-1]/(ha[0:-2]-ha[1:-1]))#find first order derivitive
accela = dVdh*dhdt[0:-2]


plt.figure()
plt.plot(ha,Va)
plt.xlabel('Altitude (m)')
plt.ylabel('Velocity (m/s)')
plt.grid()

plt.figure()
plt.plot(ha[0:-2],accela/9.81)
plt.xlabel('Time (sec)')
plt.ylabel('Gs')
plt.grid()
plt.show()
