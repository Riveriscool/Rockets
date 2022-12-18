#ballistic reentry in python, assuming lift is zero
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci
he = 122000.0
ha = np.linspace(0,he,100000)#100km
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

def Derivatives(t, state):
    #state vector
    V = state[0]
    h = state[1]
    gamma = state[2]
    #Density model
    rho = rhos*np.exp(-beta*h)
    #Aerodynamic model
    L = 0
    
    D = 0.5*rho*V**2*S*CD
    #Gravity Model
    gs = 9.81
    g = gs*(R/(r+h))**2
    r = R + h
    
    #Dynamics
    dvdt = -D/m - g*np.sin(gamma)
    dgammadt = (L/m - (g-V**2/r)*np.cos(gamma))/V
    dhdt = V*np.sin(gamma)
    
    statedot = np.asarray([dvdt,dhdt,dgammadt])
    
    return statedot
#integrate with odeint

stateinitial = np.asarray([Ve,he,gammae])
tout = np.linspace(0,100,1000)
stateout = sci.odeint(Derivatives,stateinitial,tout)

Vnum = stateout[:,0]
hnum = stateout[:,1]
gammanum = stateout[:,2]
accelnum = (Vnum[0:-2]-Vnum[1:-1])/(tout[0:2]-tout[1:-1])

plt.figure()
plt.plot(ha,Va,label='Analytic')
plt.plot(hnum,Vnum,label='Numerical')
plt.xlabel('Altitude (m)')
plt.ylabel('Velocity (m/s)')
plt.grid()

plt.figure()
plt.plot(ha[0:-2],accela/9.81,label='Analytic')
plt.plot(hnum[0:-2],accelnum/9.81,label="Numerical")
plt.xlabel('Time (sec)')
plt.ylabel('Gs')
plt.grid()
plt.show()

plt.figure()
plt.plot(tout,gammanum)
plt.ylabel('Flight path Angle (rad)')
plt.xlabel('time')
#Dear future River:
#stop being a bitch and finish this