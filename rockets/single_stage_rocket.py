
#hii
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
#Rplanet = 6357000
Rplanet = 600000
mplanet = 5.291518*10**22
#mass of planet
#mplanet = 5.972e24 # kg
#mass of rocket
weighttons = 5.3
mass0 = weighttons*2000.0/2.2#make the rocket unrealistic so it can get to orbit
#max thrust of rocket
#max_thrust = int(input("what is the max thrust?"))
max_thrust = 167970
#Gravatitational Acceleration model
#Isp = int(input("isp?"))#say 200
Isp = 250.0
#time that it burn fuel before it runs out
#tMECO = int(input("tMECO?"))# say 20
tMECO = 38.0
#initial conditions for single stage rocket
x0 = Rplanet
z0 = 0.0
velz0 = 0.0
velx0 = 0.0
period = 500.0
def gravity(x,z):
    global Rplanet,mplanet,G
    #norm of vector from center of planet to rocket
    r = np.sqrt(x**2 + z**2)
    if r < Rplanet:
        accelx = 0.0
        accelz = 0.0
    else:
        accelx = G*mplanet/(r**3)*x
        accelz = G*mplanet/(r**3)*z
    return np.asarray([accelx,accelz])

def propulsion(t):
    global max_thrust,Isp,tMECO
    if t < tMECO:
        thrustF = max_thrust
        
    else:
        thrustF = 0.0
    theta = 10.0*np.pi/180.00
    thrustx = thrustF*np.cos(theta)
    thrustz = thrustF*np.sin(theta)
    
    #mdot
    ve = Isp*9.81
    mdot = -thrustF/ve
    
    return np.asarray([thrustx,thrustz]),mdot
def Derivitives(state, t):
    #globals
    
    #state vector
    #x is altitude from center of planet along equator
    x = state[0]
    z = state[1]
    velx = state[2]
    velz = state[3]
    mass = state[4]    
    #compute zdot- Kinematic Relationship
    
    zdot = velz
    xdot = velx
    
    #compute Acceleration
    
    #Compute total force
    #z cord needs to be in reference to center of planet
    gravityF = -gravity(x,z)*mass
    aeroF = np.asarray([0.0,00.0])
    
    thrustF,mdot = propulsion(t)
    
    Forces = gravityF + aeroF + thrustF  
    if mass > 0:
        ddot = Forces/mass
    else:
        ddot = 0.0
        mdot = 0.0
    
    
    
    #compute acceleration
    ddot = Forces/mass
    
    #compute the statedot
    
    statedot = np.asarray([xdot,zdot,ddot[0],ddot[1],mdot])
    
    return statedot
#Main Script:

#Initial conditions -- For orbit
"""
x0 = Rplanet + 600000 # to orbit, you need to go up 600,000 m
z0 = 0.0
r0 = np.sqrt(x0**2 +z0*82)
#compute perfect orbiting velocity to maintain orbit
velz0 = np.sqrt(G*mplanet/r0) * 1.1# 1.1 makes it eliptic 
velx0 = 0.0
"""

stateinitial = np.asarray([x0,z0,velx0,velz0,mass0])

#time window
#compute period of orbit
"""
period = 2*np.pi/np.sqrt(G*mplanet)*r0**(3.0/2.0)#semi-major-axis of orbit is r0
period *= 1.5#to make the orbit eliptical and not circular
"""
tout = np.linspace(0,period,1000)#kepler equasion to tell how long an orbit takes

stateout = sci.odeint(Derivitives,stateinitial,tout)


#Rename variables
xout = stateout[:,0]
zout = stateout[:,1]
altitude = np.sqrt(xout**2+zout**2) - Rplanet
velxout = stateout[:,2]
velzout = stateout[:,3]
velout = np.sqrt(velxout**2 + velzout**2)
massout = stateout[:,4]

#ALTITUDE
plt.figure("Altitude V time")
plt.plot(tout,altitude)
plt.xlabel('Time (sec)')
plt.ylabel("altitude (m)")
plt.grid()
plt.show()
#VELOCITY
plt.figure("Velocity v Time")
plt.plot(tout, velout)
plt.xlabel('Time (sec)')
plt.ylabel('total Speed(m/s)')
plt.grid()
plt.show()

##Mass
plt.figure()
plt.plot(tout,massout)
plt.title("Mass V time")
plt.xlabel("Time (sec)")
plt.ylabel("Mass(kg)")
plt.grid()
#2d orbit
plt.figure()
plt.plot(xout,zout,"r-",label='Orbit')
#plot initial conditions
plt.plot(zout[0],zout[0], 'g-')
#parametric equasion for circle
theta = np.linspace(0,2*np.pi,1000)
xplanet = Rplanet*np.sin(theta)
yplanet = Rplanet*np.cos(theta)
plt.plot(xplanet,yplanet)
plt.plot(xplanet,yplanet,"b-",label="Planet")
plt.grid()
plt.legend
plt.show()
