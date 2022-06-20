# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 23:13:48 2021

@author: Lumirevel
"""

from vector import *
import turtle
turtle.setup(700,700)
turtle.colormode(255)
turtle.clear()
turtle.ht()
turtle.pu()
turtle.speed(0)
turtle.getscreen().bgcolor(30,30,30)
def circle(r,p=vector(0,0)):
    start=vector(0,-r)+p
    turtle.goto(*start)
    turtle.pd()
    turtle.begin_fill()
    turtle.circle(r)
    turtle.end_fill()
    turtle.pu()
def dot(p,col):
    turtle.goto(*p)
    turtle.dot(10,col)

import math
sin,cos,tan=math.sin,math.cos,math.tan
cot=lambda x:1/tan(x)
acos,atan2=math.acos,math.atan2
pi=math.pi

c=299792458
G=6.67430*10**(-11)
dlam=0.01#0.0001

conv=lambda r,theta,phi:r*vector(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))

class Progress:
    def __init__(self,s,e):
        self.s,self.e=s,e
    def __call__(self,i):
        return self.s+(self.e-self.s)*i

class Cam:
    def __init__(self,p,resol=300,d=150):
        self.p=vector(*p)
        
        self.f=conv(1,pi/2,pi)
        self.planex=conv(1,pi/2,3/2*pi)
        self.planey=conv(1,0,pi)
        
        self.w,self.h=700,700
        self.d=d
        
        w=Progress(-self.w/2,self.w/2)
        h=Progress(-self.h/2,self.h/2)
        
        theta=lambda i:pi/2-atan2(h(i),d)
        phi=lambda i:pi+atan2(w(i),d)
        
        self.lights=[]
        for k1 in range(resol):
            i1=k1/resol
            for k2 in range(resol):
                i2=k2/resol
                v=vector(theta(i1),phi(i2))
                co=vector(w(i2),h(i1))
                self.lights.append(Lux(p,v,co))
    
    def caculbl(self,b):
        r=b.rs*self.d/abs(self.p)
        cache=self.cacul(-self.p)
        if cache:
            circle(r,cache)
    def cacul(self,pvec):
        f=pvec*self.f
        
        if f>0:
            norm=self.d/f
            x=pvec*self.planex
            y=pvec*self.planey
            return norm*vector(x,y)
    def blit(self,b):
        for lx in self.lights:
            if not lx.stop:
                lx.cacul(b)
                col=b.disk.detect(lx)
                if col!=None:
                    dot(lx.co,col)#self.cacul(lx.sv),col)
                    lx.stop=True


class Black:
    def __init__(self,M=10**35,rcp=5.5,h=3*10**6):
        self.M=M
        rs=self.rs=G*self.M/c**2
        self.disk=Disk(rs,rcp,h)
    def blit(self,cam):
        cam.caculbl(self)

class Disk:
    def __init__(self,rs,rcp,h=3000000):
        self.rs,self.re,self.maxh=rs,rs*rcp,h
        s=vector(245,158,11)
        e=vector(239,68,68)
        self.col=Progress(s,e)
    def detect(self,lx):
        x,y,z=conv(*lx.p[1:3+1])
        x0,y0,z0=conv(*lx.p0[1:3+1])
        h=self.maxh
        #if abs(z)<h:
        if (z-h)*(z0-h)<0 or (z+h)*(z0+h)<0:
            try:
                d=math.sqrt(x**2+y**2)
                """
                if d<=self.rs:
                    print("wow")
                    return vector(0,0,0)
                """
                if d<self.re:
                    i=(d-self.rs)/(self.re-self.rs)
                    return self.col(i.quant())
            except:
                lx.stop=True

class Lux:
    def __init__(self,p,v,co=(0,0)):
        t,x,y,z=0,*p
        
        r=abs(p)
        theta=acos(z/r)
        phi=atan2(y,x)
        
        self.p0=self.p=vector(t,r,theta,phi)
        
        stheta,sphi=v
        sv=self.sv=conv(c,stheta,sphi)
        self.co=co
        
        rvec=vector(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))
        thetavec=vector(cos(theta)*cos(phi),cos(theta)*sin(phi),-sin(theta))
        phivec=vector(-sin(phi),cos(phi),0)
        
        dt=0.1#0.00001
        dr=sv*rvec
        dtheta=sv*thetavec/r
        dphi=sv*phivec/(r*sin(theta))
        
        self.v=vector(dt,dr,dtheta,dphi)
        self.stop=False
    def cacul(self,b):
        t,r,theta,phi=self.p
        w=1-b.rs/r
        if w>0:
            theta%=math.tau
            theta=min(theta,math.tau-theta)
            phi%=math.tau
            try:
                dt,dr,dtheta,dphi=self.v
                dw=b.rs/r**2
                drpr=dr/r
                
                ddt=-dw/w*dr*dt
                ddr=w*(r*(dtheta**2+(dphi*sin(theta))**2)+dw*((dr/w)**2-(c*dt)**2)/2)
                ddtheta=sin(2*theta)/2*dphi**2-2*drpr*dtheta
                ddphi=-2*(drpr+dtheta*cot(theta))*dphi
                a=vector(ddt,ddr,ddtheta,ddphi)
                
                self.v+=a*dlam
                self.p0=self.p
                self.p+=self.v*dlam
            except:
                self.stop=True
        else:
            self.stop=True


b=Black()
p=vector(5*b.rs,0*b.rs,0.5*b.rs)
cam=Cam(p,25)
b.blit(cam)

turtle.tracer(625)

step=1000
for i in range(step):
    cam.blit(b)
    print(f'{round(i/step*100,1)}%')
