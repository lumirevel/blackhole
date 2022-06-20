import math
from UI import *
from vector import vector
from matrix import matrix
from viewer import Window, Movie

#game window 설정
game=Window()

sin,cos,tan=math.sin,math.cos,math.tan
cot=lambda x:1/tan(x)
acos,atan2=math.acos,math.atan2
pi=math.pi

conv=lambda r,theta,phi:r*vector(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))

class Space:
    c=299792458
    G=6.67430*10**-11
    dlam=0.01

class Cam:
    def __init__(self,p,resol=300,d=300):
        self.p=vector(*p)
        
        the=0
        self.f=conv(1,pi/2+the,pi)
        self.planex=conv(1,pi/2,3/2*pi)
        self.planey=conv(1,0+the,pi)
        
        self.w,self.h=game.window_size
        self.d=d
        
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
        self.pars=[]
    
    def caculbl(self,b,window):
        r=b.rs*self.d/abs(self.p)
        cache=self.cacul(-self.p)
        if cache:
            try:
                Ball(r).pos(*cache).blit(window)
            except TypeError:
                pass
    def cacul(self,pvec):
        f=pvec*self.f
        if f>0:
            norm=self.d/f
            x=pvec*self.planex
            y=pvec*self.planey
            return norm*vector(x,y)
    def blit(self,b,window):
        for i, lx in enumerate(self.lights):
            if not lx.stop:
                lx.cacul(b)
                b.disk.detect(lx)
                if lx.col!=None:
                    self.pars=[self.lights.pop(i)]+self.pars
        for lx in self.pars:
            Ball(1).pos(*lx.co).col(*lx.col).blit(window)


class Black:
    def __init__(self,M=10**35,rcp=5.5,h=3*10**6):
        self.M=M
        rs=self.rs=Space.G*self.M/Space.c**2
        self.disk=Disk(rs,rcp,h)
    def blit(self,cam,window):
        cam.caculbl(self,window)

class Disk:
    def __init__(self,rs,rcp,h=3000000):
        self.rs,self.re,self.he=rs,rs*rcp,h
        s,e=vector(245,158,11),vector(239,68,68)
        self.col=Progress(s,e)
    def detect(self,lx):
        x,y,z=conv(*lx.p[1:3+1])
        x0,y0,z0=conv(*lx.p0[1:3+1])
        if (z-self.he)*(z0-self.he)<0 or (z+self.he)*(z0+self.he)<0:
            try:
                d=math.sqrt(x**2+y**2)
                
                if d<self.rs:
                    lx.col=vector(0,0,0)
                    lx.stop=True
                elif d<self.re:
                    i=(d-self.rs)/(self.re-self.rs)
                    lx.col=self.col(i)
                    lx.stop=True
            except OverflowError:
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
        if r>0:
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
            except OverflowError:
                self.stop=True
        else:
            self.stop=True

class Play(Movie):
    def __init__(self):
        self.b=Black()
        p=vector(10*self.b.rs,0*self.b.rs,0.5*self.b.rs)
        self.cam=Cam(p,50)
    def main(self,window):
        self.b.blit(self.cam,window)
        self.cam.blit(self.b,window)
        
game.addscene(Play())
game.main()