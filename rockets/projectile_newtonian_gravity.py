import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci



#equasions of motion
#F = m*a = M*second-derivitive of altitude = zddot*m
#z-cord for now is altitude of the surface
#im meters
#zddot = acceleration

#constant parameters

#gravitational consatant
G = 6.6743*10**-11
#radius of planet
Rplanet = 6357000
#mass of planet
mplanet = 5.972e24 # kg
#mass of rocket
mass = 640.0/1000.0

#Gravatitational Acceleration model
def gravity(z):
    global Rplanet,mplanet
    #norm of vector from center of planet to rocket
    r = np.sqrt(z**2)
    if r < Rplanet:
        accel = 0.0
    else:
        accel = G*mplanet/(r**3)*r
    return accel


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
    #z cord needs to be in reference to center of planet
    gravityF = -gravity(z)*mass
    aeroF = 0.0
    
    thrustF = 0.0
    
    
    Forces = gravityF + aeroF + thrustF  
    #compute acceleration
    zddot = Forces/mass
    
    #compute the statedot
    
    statedot = np.asarray([zdot,zddot])
    
    return statedot
#Main Script:

#Initial conditions
z0 = Rplanet
velz0 = 164.0
stateinitial = np.asarray([z0,velz0])


#time window

tout = np.linspace(0,35,1000)

stateout = sci.odeint(Derivitives,stateinitial,tout)


#Rename variables
zout = stateout[:,0]
altitude = zout - Rplanet
velzout = stateout[:,1]

#ALTITUDE
plt.figure("Altitude V time")
plt.plot(tout,altitude)
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
