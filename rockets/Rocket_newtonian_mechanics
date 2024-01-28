import time as t
import numpy as np
import matplotlib.pyplot as plt
import turtle 

wn = turtle.Screen()
wn.title("sim")


rc = turtle.Turtle()
rc.shape("circle")
rc.shapesize(1,2)
rc.color("orange")

class Rocket:
    def __init__(self,xcor,ycor,zcor,mass,sthrust,𝜃,buf,mthrust1,mthrust2,tmeco1,tmeco2,CD):
        self.xcor = xcor
        self.ycor = ycor
        self.zcor = zcor
        self.mass = mass
        self.sthrust = sthrust
        self.𝜃 = 𝜃
        self.mthrust1 = mthrust1
        self.mthrust2 = mthrust2
        self.tmeco1 = tmeco1
        self.buf = buf
        self.tmeco2 = tmeco2
        self.CD = CD
        self.ΣFx = 0
        self.ΣFy = 0
        self.ΣFz = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.rot_vel = 0
        self.ΣFr = 0
        self.mthrust1_x,self.mthrust1_z = np.cos(self.𝜃)*mthrust1,np.sin(self.𝜃)*mthrust1
        self.mthrust2_x,self.mthrust2_z = np.cos(self.𝜃)*mthrust2,np.sin(self.𝜃)*mthrust2
        self.xcors = [0]
        self.ycors = [0]
        self.zcors = [0]
        self.rot_vels = [0]
        self.thetas = [0]
        self.vxs = [0]
        self.vys = [0]
        self.vzs = [0]
        self.fxs = [0]
        self.fys = [0]
        self.fzs = [0]
        self.axs = [0]
        self.ays = [0]
        self.azs = [0]
        self.Frs = [0]
        self.times = [0]
        self.lthrust = False
        self.rthrust = False



    def graph(self,title,y):
        plt.figure()
        plt.title(title)
        plt.plot(self.times,y)
        plt.show()

    def main_thrust_components_1(self):
        return (np.cos(self.𝜃)*self.mthrust1, np.sin(self.𝜃)*self.mthrust1)
    def main_thrust_components_2(self):
        return (np.cos(self.𝜃)*self.mthrust2, np.sin(self.𝜃)*self.mthrust2)
    def launch(self):
        time = 0
        print("launching...")
        stopped = False
        while not stopped:
            time += 1
            #calc net forces

            if self.tmeco1 > 0:
                self.ΣFx += self.mthrust1_x
                self.ΣFz+= self.mthrust1_z 
                self.tmeco1 -= 1
                self.rthrust = True
                print("tmeco1")
            
            if self.buf > 0 and self.tmeco1 == 0:
                turn_right = True
                turn_left = False
                self.ΣFz = -9.8 * self.mass
                buffering = True
                self.buf -= 1
                print("buffering")
                
            if self.tmeco1 == 0 and self.buf == 0 and self.tmeco2 > 0:
                self.ΣFx += self.mthrust2_x- (9.8*self.mass)
                self.ΣFz += self.mthrust2_z
                self.tmeco2 -= 1
                print("tmeco2")
            
            if self.lthrust == True:
                self.ΣFr -= 45
            if self.rthrust == True:
                self.ΣFr += 45

            self.ΣFx -= 9.8*self.mass
            self.ΣFr -= self.ΣFr / 10
            self.fxs.append(self.ΣFx) 
            self.fys.append(self.ΣFy)
            self.fzs.append(self.ΣFz)
            self.Frs.append(self.ΣFr)
            #calc accelerations
            self.ax = self.ΣFx / self.mass
            self.ay = self.ΣFy / self.mass
            self.az = self.ΣFz / self.mass
            self.ar = self.ΣFr / self.mass
            self.axs.append(self.ax)
            self.ays.append(self.ay)
            self.azs.append(self.az)
            #calc velocities
            self.vx += self.ax
            self.vy += self.ay
            self.vz += self.az
            if turn_right == True:
                self.rot_vel = (burn_rate*fperkg*dist)/(totalmass_distance**2)
            elif turn_left == True:
                pass
            else:
                self.rot_vel += self.ar
            self.vxs.append(self.vx)
            self.vys.append(self.vy)
            self.vzs.append(self.vz)
            #calc position
            self.xcor = self.xcor + self.vx
            self.ycor = self.ycor + self.vy
            self.zcor = self.zcor + self.vz
            self.xcors.append(self.xcor)
            self.ycors.append(self.ycor)
            self.zcors.append(self.zcor)
            rc.goto(self.xcor/10,self.zcor/100)
            rc.setheading(self.𝜃)
            #change angle
            self.𝜃 += self.ar
            print(self.xcor,self.ycor,self.zcor)
            self.ΣFx,self.ΣFy,self.ΣFz,self.rthrust = 0,0,0,False

            #update lists
            self.thetas.append(self.𝜃)       
            self.rot_vels.append(self.rot_vel)

            if self.zcor < 0:
                stopped = True

            self.times.append(time)
        print(self.times,self.xcors,self.ycors,self.zcors,self.vxs,self.vys,self.vzs,self.axs,self.ays,self.azs,self.thetas,self.rot_vels,self.fxs,self.fys,self.fzs,self.Frs)
        self.graph("Ycor v time", self.ycors)
        self.graph("Zcor v time",self.zcors)
        self.graph("X velocity v time",self.vxs)
        self.graph("Y velocity V time",self.vys)
        self.graph("Z velocity v time",self.vzs)
        self.graph("Acceleration in the X direction",self.axs)
        self.graph("Acceleration in theh Y direction",self.ays)
        self.graph("Acceleration in the Z direction", self.azs)
        self.graph("Rocket Angle V time", self.thetas)
        self.graph("Rotational velocity V time",self.rot_vels)
        self.graph("Net Force in the X direction V time",self.fxs)
        self.graph("Net Force in the Y direction V time",self.fys)
        self.graph("Net Force in the Z direction V time",self.fzs)
        self.graph("Centripital Force V time",self.Frs)


r = Rocket(0,0,0,2,30,45,10,500,50,5,5,3)
r.launch()
"""matrix = r.launch()
(times,xcors,ycors,zcors,vxs,vys,vzs,axs,ays,azs,thetas,rot_vels,fxs,fys,fzs,frs) = matrix

plt.figure()
plt.plot(times,xcors)
"""
