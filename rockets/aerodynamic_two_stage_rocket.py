
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
Isp1 = 250.0
#time that it burn fuel before it runs out
#tMECO = int(input("tMECO?"))# say 20
Isp2 = 400.0
tMECO = 38.0
#length of time to remove 1st stage
tsep1 = 2.0
#mass of first stage
mass1tons = 0.2
mass1 = mass1tons*2000/2.2
t2start = 261.0
t2end = t2start + 17.5#make it 20 to get far enough so air resistance doesnt matter

#initial conditions for single stage rocket
x0 = Rplanet
z0 = 0.0
velz0 = 0.0
velx0 = 0.0
r0 = 200000 + Rplanet
period = 2*np.pi/np.sqrt(G*mplanet)*r0**(3.0/2.0)#semi-major-axis of orbit is r0
period *= 1.5#to make the orbit eliptical and not circular
period = 12000
Diamater = 0.85
#S = np.pi*(Diamater/2.0)**2#cross-sectional area
CD = 0.1

class Aerodynamics():
    def __init__(self,name):
        self.name = name
        if name == "Kerbin":
            data = np.loadtxt('kerbin_aerodynamics.txt')
            #print(data)
            self.altitude = data[:,0]
            #print(self.altitude)
            self.density = data[:,3]
            #print(self.density)
            self.rohs = self.density[0]
            self.beta = 0.0
        elif name == "Earth":
           self.beta = 0.1354/1000.0
           self.rohs = 1.225
    def getDensity(self,altitude):
        if self.name == "Kerbin":
            rho = np.interp(altitude,self.altitude,self.density)
        elif self.name == 'Earth':
            rho = self.rhos*np.exp(-self.beta*altitude)
        return rho
            
#planet
name = 'Kerbin'
aeroModel = Aerodynamics(name)
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
    return np.asarray([accelx,accelz]),r

def propulsion(t):
    global max_thrust,Isp,tMECO,ve
    #Timing for thrusters
    if t < tMECO:
        theta = 10*np.pi/180.0
        thrustF = max_thrust  
        ve = Isp1*9.81
        mdot = -thrustF/ve     
        
    if t > tMECO and t < (tMECO + tsep1):
        theta = 0.0
        thrustF = 0.0
        mdot = -mass1/tsep1
    if t > (tMECO + tsep1):
        theta = 0.0 
        thrustF = 0.0
        mdot = 0.0
    if t > (t2start) and t < (t2end):
        theta = 90.0*np.pi/180.0
        thrustF = max_thrust
        ve = Isp2*9.81
        mdot = -thrustF/ve
        
    if t > t2end:
        theta = 0.0
        thrustF = 0.0
        mdot = 0.0
        
 
    thrustx = thrustF*np.cos(theta)
    thrustz = thrustF*np.sin(theta)
    
    #mdot

    
    return np.asarray([thrustx,thrustz]),mdot
def Derivitives(state, t):
    #globals
    global aeroModel
    global Rplanet
    
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
    accel,r = gravity(x,z)
    gravityF = -accel*mass
    
    #Aerodynamics
    
    altitude = r - Rplanet
    rho = aeroModel.getDensity(altitude)#air density
    V = np.sqrt(velz**2+velx**2)
    aeroF = np.asarray([0.0,00.0])
    qinf = (np.pi/8.0)*rho*(Diamater**2)*abs(V)
    aeroF = -qinf*CD*np.asarray([velx,velz])
    
    
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
#Plot the air density as a function of AGL
test_altitude = np.linspace(1,100000,100)
test_rho = aeroModel.getDensity(test_altitude)
plt.figure()
plt.plot(test_altitude,test_rho,'-b')
plt.xlabel('altitude(m)')
plt.ylabel('Air density (kg/m^3)')
plt.grid()

#Initial conditions -- For orbit
"""
x0 = Rplanet + 600000 # to orbit, you need to go up 600,000 m
z0 = 0.0
r0 = np.sqrt(x0**2 +z0*82)
#compute perfect orbiting velocity to maintain orbit
velz0 = np.sqrt(G*mplanet/r0) * 1.1# 1.1 makes it eliptic 
velx0 = 0.0
"""
#Compute Exit Velocity

#Populate initial condition vector
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
