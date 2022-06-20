# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 23:55:36 2021

@author: Lumirevel
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 22:06:04 2021

@author: Lumirevel
"""

import math

from vector import vector
from matrix import matrix
import turtle
turtle.ht()
turtle.pu()
turtle.speed(0)
turtle.getscreen().bgcolor(*vector(30,30,30)/255)
def dot(p,col):
    turtle.goto(*p)
    turtle.dot(1,col)

class Progress:
    def __init__(self,s,e):
        self.s,self.e=s,e
    def __call__(self,i):
        return self.s+(self.e-self.s)*i

sin,cos,tan=math.sin,math.cos,math.tan
cot=lambda x:1/tan(x)
acos,atan2=math.acos,math.atan2
pi=math.pi

conv=lambda r,theta,phi:r*vector(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))

def hsv2rgb(h,s,v):
    H=h
    S=s/255
    V=v/255
    C=V*S
    X=C*(1-abs((h/60)%2-1))
    m=V-C
    RGB=(0,1,1)
    if H>=0 and H<60:
        RGB= (C,X,0)
    elif H>=60 and H<120:
        RGB= (X,C,0)
    elif H>=120 and H<180:
        RGB= (0,C,X)
    elif H>=180 and H<240:
        RGB= (0,X,C)
    elif H>=240 and H<300:
        RGB= (X,0,C)
    elif H>=300 and H<360:
        RGB= (C,0,X)
    return RGB[0]+m,RGB[1]+m,RGB[2]+m

def rgb2hex(rgb):
    r=int(rgb[0])#rgb의 r값
    g=int(rgb[1])#rgb의 g값
    b=int(rgb[2])#rgb의 b값
    return "#"+hex(r).replace("0x","").zfill(2)+hex(g).replace("0x","").zfill(2)+hex(b).replace("0x","").zfill(2)#rgb값 각각 hex코드로 변환 후 합침(replace는 hex형식으로 변환시 '0x'가 붙는 것을 없애는 용도, zfill은 hex값이 한 자리 수일 때 0을 추가함

def lamda2rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength*10**9)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255
    return (int(R), int(G), int(B))

def T2rgb(T):
    '''
    Start with a temperature, in Kelvin, somewhere between 1000 and 40000.  (Other values may work,
    but I can't make any promises about the quality of the algorithm's estimates above 40000 K.)
    Note also that the temperature and color variables need to be declared as floating-point.
    '''
    Temperature = T/100
    
    if Temperature <= 66:
    	Red = 255
    else:
    	Red = Temperature - 60
    	Red = 329.698727446 * (Red ** -0.1332047592)
    	Red=min(max(0,Red),255)
    
    if Temperature <= 66:
    	Green = Temperature
    	Green = 99.4708025861 * math.log(Green) - 161.1195681661
    else:
    	Green = Temperature - 60
    	Green = 288.1221695283 * (Green ** -0.0755148492)
    Green=min(max(0,Green),255)
    
    if Temperature >= 66:
    	Blue = 255
    elif Temperature <= 19:
    	Blue = 0
    else:
        Blue = Temperature - 10
        Blue = 138.5177312231 * math.log(Blue) - 305.0447927307
        Blue=min(max(0,Blue),255)
    return (Red,Green,Blue)

class Space:
    c=299792458
    G=6.67430*10**-11
    k=1.38*10**-23
    h=6.62607015*10-34
    b=2.897771955*10**-3
    dlam=0.01

class Cam:
    def __init__(self,p,resol=300,d=300):
        self.p=vector(*p)
        
        the=0
        self.f=conv(1,pi/2+the,pi)
        self.planex=conv(1,pi/2,3/2*pi)
        self.planey=conv(1,0+the,pi)
        
        self.w,self.h=(700,700)#game.window_size
        self.d=d
        
        #self.surf= np.full((700, 700, 3),0)
        
        w,h=Progress(-self.w/2,self.w/2),Progress(-self.h/2,self.h/2)
        theta,phi=lambda i:pi/2-atan2(h(i),d)+the,lambda i:pi+atan2(w(i),d)
        
        self.lights=[]
        for k1 in range(resol):
            i1=k1/resol
            for k2 in range(resol):
                i2=k2/resol
                v=vector(theta(i1),phi(i2))
                co=vector(w(i2),h(i1))
                self.lights.append(Lux(p,v,co))
        print('start')
        
        self.steplights=0
        self.step=0
        
    
    def caculbl(self,b):
        r=b.rs*self.d/abs(self.p)
        cache=self.cacul(-self.p)
        if cache:
            try:
                pass#turtle.circle(r).pos(*cache).blit(window)
            except TypeError:
                pass
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
                b.disk.detect(lx,self)
                if lx.col!=None:
                    dot(lx.co,vector(lx.col)/255)
                    #x,y=window.pos2scr(lx.co)
                    #self.surf[int(x-1),int(y-1),:]=lx.col
                    #pygame.surfarray.blit_array(window.screen,self.surf)
                    #pygame.display.update()
                    self.lights.pop(self.steplights)
                    self.steplights-=1
            
            self.steplights+=1
            if self.steplights==len(self.lights):
                self.steplights=0
                self.step+=1
                if self.step%10==0:
                    print(self.step)


class Black:
    def __init__(self,M=10**35,rcp=6,h=3*10**6):#rcp=5.5
        self.M=M
        rs=self.rs=2*Space.G*self.M/Space.c**2
        self.disk=Disk(rs,rcp,h)
    def blit(self,cam,window):
        cam.caculbl(self)

class Disk:
    def __init__(self,rs,rcp,h=3000000):
        self.rs,self.re,self.he=rs,rs*rcp,h
        #s,e=vector(245,158,11),vector(239,68,68)
        #self.col=Progress(s,e)
    def detect(self,lx,cam):
        x,y,z=conv(*lx.p[1:3+1])
        x0,y0,z0=conv(*lx.p0[1:3+1])
        if (z-self.he)*(z0-self.he)<0 or (z+self.he)*(z0+self.he)<0:
            try:
                d=math.sqrt(x**2+y**2)
                if d<self.rs:
                    lx.col=vector(0,0,0)
                    lx.stop=True
                elif d<self.re:
                    """
                    #i=(d-self.rs)/(self.re-self.rs)
                    T=self.rs*Space.c**2/(3*Space.k*d)
                    H=colorsys.rgb_to_hsv(*T2rgb(T))[0]*360
                    L=(650-250/270*H)*10**-9
                    lamdas=L#Space.b/T
                    
                    rsf=lambda r:1-self.rs/r
                    v=math.sqrt(self.rs*Space.c**2/2/d)
                    phivec=vector(-sin(lx.p[3]),cos(lx.p[3]),0)
                    v=v*phivec
                    direct=conv(*lx.v[1:3+1]).unit
                    beta=v*direct/Space.c
                    ratio=math.sqrt((1+beta)/(1-beta))
                    
                    lamda=ratio*lamdas*math.sqrt(rsf(abs(cam.p))/rsf(d))
                    """
                    #source
                    absv=math.sqrt(self.rs*Space.c**2/2/d)
                    phivec=vector(-sin(lx.p[3]),cos(lx.p[3]),0)
                    v=absv*phivec
                    
                    self.rs<2*d
                    
                    direct=conv(*lx.v[1:3+1]).unit
                    beta=v*direct/Space.c
                    
                    T=self.rs*Space.c**2/(3*Space.k*d)
                    Tprime=T*math.sqrt((1-beta)/(1+beta))
                    
                    maxlamda=Space.h*Space.c/(4.97*Space.k*Tprime)
                    
                    I = lambda lamda,T:2*Space.h*Space.c**2/(lamda**5*(math.exp(Space.h*Space.c/(lamda*Space.k*T))-1))
                    
                    if maxlamda<380*10**-9:
                        lamda=380*10**-9
                    elif maxlamda>750*10**-9:
                        lamda=750*10**-9
                    else:
                        lamda=maxlamda
                    i=I(lamda,Tprime)/abs(cam.p-vector(x,y,z))**2
                    lx.col=lamda2rgb(lamda)#T2rgb(T)#self.col(i)
                    lx.stop=True
            except OverflowError as e:
                lx.stop=True

class Lux:
    def __init__(self,p,v,co=(0,0)):
        t,x,y,z=0,*p
        
        r=abs(p)
        theta=acos(z/r)
        phi=atan2(y,x)
        
        self.p0=self.p=vector(t,r,theta,phi)
        
        stheta,sphi=v
        sv=self.sv=conv(Space.c,stheta,sphi)
        self.co=co
        
        rvec=vector(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))
        thetavec=vector(cos(theta)*cos(phi),cos(theta)*sin(phi),-sin(theta))
        phivec=vector(-sin(phi),cos(phi),0)
        
        dt,dr,dtheta,dphi=0.1,*matrix(rvec,thetavec/r,phivec/(r*sin(theta)))*sv
        self.v=vector(dt,dr,dtheta,dphi)
        
        self.stop=False
        self.col=None
    def cacul(self,b):
        t,r,theta,phi=self.p
        if 0<r<2*b.disk.re:
            theta%=math.tau
            theta=min(theta,math.tau-theta)
            phi%=math.tau
            try:
                dt,dr,dtheta,dphi=self.v
                w=1-b.rs/r
                dw=b.rs/r**2
                drpr=dr/r
                
                ddt=-dw/w*dr*dt
                ddr=w*(r*(dtheta**2+(dphi*sin(theta))**2)+dw*((dr/w)**2-(Space.c*dt)**2)/2)
                ddtheta=sin(2*theta)/2*dphi**2-2*drpr*dtheta
                ddphi=-2*(drpr+dtheta*cot(theta))*dphi
                a=vector(ddt,ddr,ddtheta,ddphi)
                
                self.v+=a*Space.dlam
                self.p0=self.p
                self.p+=self.v*Space.dlam
            except OverflowError as e:
                self.stop=True
        else:
            self.stop=True

b=Black()
p=vector(7*b.rs,0*b.rs,0.1*b.rs)#10,0,0.5
cam=Cam(p,200)

for i in range(10000):
    cam.blit(b)
    
'''
class Play(Movie):
    def __init__(self):
        self.b=Black()
        p=vector(7*self.b.rs,0*self.b.rs,0.1*self.b.rs)#10,0,0.5
        self.cam=Cam(p,200)
    def main(self,window):
        #self.b.blit(self.cam,window)
        self.cam.blit(self.b,window)
'''

#game.addscene(Play())
#game.main()