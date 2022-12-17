# brb    
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci



#equasions of motion
#F = m*a = M*second-derivitive of altitude = zddot*m
#z-cord for now is altitude of the surface
#im meters
#zddot = acceleration
#constant parameters

mass = 640.0/1000.0
def Derivitives(state, t):
    #globals
    global mass
    #state vector
    z = state[0]
    velz = state[1]
    #compute zdot- Kinematic Relationship
    
    zdot = velz
    
    #compute Acceleration
    
    #Compute total force
    gravity = -9.81*mass
    aero = 0.0
    
    thrust = 0.0
    
    
    Forces = gravity + aero + thrust    
    #compute acceleration
    zddot = Forces/mass
    
    #compute the statedot
    
    statedot = np.asarray([zdot,zddot])
    
    return statedot
#Main Script:

#Initial conditions
z0 = 0.0
velz0 = 164.0
stateinitial = np.asarray([z0,velz0])


#time window

tout = np.linspace(0,35,1000)

stateout = sci.odeint(Derivitives,stateinitial,tout)


#Rename variables
zout = stateout[:,0]
velzout = stateout[:,1]

#ALTITUDE
plt.figure("Altitude V time")
plt.plot(tout,zout)
plt.xlabel('Time (sec)')
plt.ylabel("altitude (m)")
plt.grid()
plt.show()
#VELOCITY
plt.figure("Velocity v Time")
plt.plot(tout, velzout)
plt.xlabel('Time (sec)')
plt.ylabel('Normal Speed(m/s)')
plt.grid()
plt.show()
