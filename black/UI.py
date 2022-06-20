# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:10:08 2020

@author: Lumirevel
"""
from vector import vector
from postEasings import *
from tools import *
from threading import Timer
import time
import pygame

class Rast:#사진파일용
    def __init__(self,img,size,pos=(0,0)):
        self.img=img
        self.pos=pos#객체 위치
        self.size=size#객체 반경
    def blit(self,screen,pos=0):#위치 업데이트
        if pos!=0:
            self.pos=pos
        screen.drawRast(self.img,self.pos)
        
class Ball:#원 객체
    def __init__(self,size,pos=(0,0),color=(0,0,0)):
        self.color=color
        self.size=size
        self.p=vector(pos)#객체 위치
    def pos(self,x,y):#가독성용
        self.p=vector(x,y)
        return self
    def col(self,r,g,b):#가독성용
        self.color=(r,g,b)
        return self
    def blit(self,screen,pos=0):#위치 업데이트
        if pos!=0:
            self.p=vector(pos)
        screen.drawBall(self.color,self.size,self.p)

class Rect:#회전 가능 직사각형 객체
    def __init__(self,size,position=(0,0),angle=0,color=(0,0,0)):
        self.color=color
        self.size=vector(size)
        self.p=vector(position)#객체 위치
        self.angle=angle
    def pos(self,x,y):#가독성용
        self.p=vector(x,y)
        return self
    def ang(self,angle):#가독성용
        self.angle=angle%360
        return self
    def col(self,r,g,b):#가독성용
        self.color=(r,g,b)
        return self
    def blit(self,screen,pos=0,ratio=1):#위치 업데이트
        if pos!=0:
            self.p=vector(pos)
        screen.drawRect(self.color,ratio*self.size,self.p,self.angle)
        

            
class Popup(Rect):#계속 떠있는 박스
    def __init__(self,size,pos=(0,0),angle=0,color=(0,0,0),other=[]):
        super().__init__(size,pos,angle,color)
        
        self.ff=FF()#볼펜처럼
        self.objs=other
    def blit(self,window,boolean=1,pos=0):#위치 업데이트
        if pos!=0:
            self.p=vector(pos)
        if self.ff(boolean):
            window.drawRect(self.color,self.size,self.p,self.angle)
            for obj in self.objs:
                obj.blit(window)
        return self.ff(boolean)

class Zip:#묶음
    def __init__(self,*subject):
        self.objs=list(subject)
    def blit(self,window):#위치 업데이트
        for obj in self.objs:
            obj.blit(window)
    def append(self,subject):
        self.objs.append(subject)
    def remove(self,index):
        self.objs.pop(index)

class Video(Rect):
    def __init__(self,size,pos=(0,0),angle=0,color=(0,0,0),func=easeInOutQuart,other=[]):
        super().__init__(size,pos,angle,color)
        self.easing=func
        self.objs=other

class Player:
    def __init__(self,video):
        self.video=video
        self.start=None
        self.isplay=False
        self.dt=None
    def play(self):
        if not self.isplay:#재생중이지 않을 때
            self.start=time.time()#시작 시간 정하기
        else:#재생중일 때
            self.dt=time.time()-self.start#재생시간
            if self.dt<self.video.length:#video가 아직 남았음
                self.video(self.dt)#나와라 참께
            else:#다 재생됐으면
                self.isplay=False#정
    def stop(self):
        self.isplay=False
        
class Banner(Rect):#잠깐 뜨다 사라지는 박스
    def __init__(self,size,pos=(0,0),angle=0,color=(0,0,0),func=easeInOutQuart,other=[]):
        super().__init__(size,pos,angle,color)
        
        self.easing=func
        self.objs=other
        
    def intro(self,window):
        self.cache_scene=window.sceneNum
        self.cache_bgcolor=window.bgcolor
        window.sceneNum=-1
        window.bgcolor=(255,255,255)
        
    def movieIn(self,window,x):
        step=0.2+0.6*x#0.2->0.8
        k=self.easing(step)
        window.drawRect(self.color,k*vector(self.size),self.p,self.angle)
        for obj in self.objs:
            obj.blit(window,ratio=k)
        pygame.display.flip()
        
    def movieOut(self,window,x):
        step=0.8-0.6*x#0.2->0.8
        k=self.easing(step)
        window.drawRect(self.color,k*vector(self.size),self.p,self.angle)
        for obj in self.objs:
            obj.blit(window,ratio=k)
        pygame.display.flip()
        
    def finale(self,window):
        window.sceneNum=self.cache_scene
        window.bgcolor=self.cache_bgcolor
        
    def blit(self,window,pos=0):#위치 업데이트
        if pos!=0:
            self.p=vector(pos)
        
        self.intro(window)#배너 장면으로
        
        #나타나기 효과
        start=time.time()
        while(1):
            dt=time.time()-start
            self.movieIn(window,dt/1.2)
            if dt>1.2:
                break
        
        #대기
        start=time.time()
        while(1):
            dt=time.time()-start
            if dt>0.6:
                break
        
        #사라지기 효과
        start=time.time()
        while(1):
            dt=time.time()-start
            self.movieOut(window,dt/1.2)
            if dt>1.2:
                break
            
        self.finale(window)#원래 장면으로
        
class Effect:#잠깐 뜨다 사라지는 박스
    def __init__(self,obj,func=easeInOutQuart):
        self.obj=obj
        self.easing=func
        
        self.startIn=Init()
        self.start=Init()
        self.startOut=Init()
        
        self.phase=1
        
    def movieIn(self,window,x):
        step=0.2+0.6*x#0.2->0.8
        k=self.easing(step)
        self.obj.blit(window,ratio=k)
    
    def movie(self,window):
        step=0.8
        k=self.easing(step)
        self.obj.blit(window,ratio=k)
    
    def movieOut(self,window,x):
        step=0.8-0.6*x#0.2->0.8
        k=self.easing(step)
        self.obj.blit(window,ratio=k)
        
    def blit(self,window):#위치 업데이트
        t=time.time()
        dt=t-self.start(t)
        if self.phase==1:
            self.movieIn(window,dt/1.2)
            if dt>1.2:
                self.phase+=1
                self.start.__init__()
        elif self.phase==2:
            self.movie(window)
            if dt>0.6:
                self.phase+=1
                self.start.__init__()
        elif self.phase==3:
            self.movieOut(window,dt/1.2)
            if dt>1.2:
                self.phase+=1
        elif self.phase==4:
            del self
              
class Text:#글자
    def __init__(self,fontname,textsize,content="",color=(0,0,0),pos=(0,0)):
        self.font=fontname
        self.size=textsize
        self.color=color
        self.content=content
        self.p=vector(pos)#객체 위치
    def siz(self,size):
        self.size=size
        return self
    def pos(self,x,y):
        self.p=vector(x,y)
        return self
    def col(self,r,g,b):
        self.color=(r,g,b)
        return self
    def cont(self,content):
        self.content=content
        return self
    def blit(self,window,pos=0,ratio=1):#위치 업데이트
        if pos!=0:
            self.p=vector(pos)
        font=pygame.font.Font(self.font,int(ratio*self.size))
        text=self.content.split("\n")#enter 가능
        n=len(text)
        for k, line in enumerate(text):
            scripten_line=font.render(line,True,self.color)
            
            ak=(n-1)/2-k#n개 일때 k번째 줄의 위치
            alpha=ratio*ak*vector(0,self.size)
            window.drawRast(scripten_line,self.p+alpha)