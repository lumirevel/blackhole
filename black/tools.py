# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:33:47 2020

@author: Lumirevel
"""

class Once:
    def __init__(self, function, args=None, kwargs=None):
        self.cache=None
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
    def __call__(self,i, args=None, kwargs=None):
        self.args = args if args is not None else self.args
        self.kwargs = kwargs if kwargs is not None else self.kwargs
        if not self.cache==i:
            self.function(*self.args, **self.kwargs)
        self.cache=i

class FF:#볼펜
    def __init__(self,state=False):
        """
        state->FF
        
        state#켜짐/꺼짐
        
        pressed#눌렸음
        toggled#토글 상태
        """
        self.pressed=False
        self.toggled=bool(state)
    def __call__(self,click):#딸깍
        """
        press#누름
        """
        press=bool(click)
        if not self.pressed:#안 눌렸음
            if press:#눌림
                self.toggled=not self.toggled#inversion
        
        self.pressed=press
        return self.toggled
    def click(self):
        self(0)
        self(1)
        return self(0)

class PS:#purse
    def __init__(self,T):
        self.T=T
        self.term=0
    def __call__(self):
        self.term+=1
        self.term%=self.T
        return bool(not self.term)
    
class TP:#tape#boost deleter
    def __init__(self,lim):
        self.lim=lim
        self.cum=0
    def __call__(self,boolean):
        if boolean:
            self.cum+=1
        else:
            self.cum=0
        return self.cum>self.lim

class Init:#반영구 데이터
    def __init__(self):
        self.data=None
    def __call__(self,data):
        if self.data==None:
            self.data=data
        return self.data
    
from copy import deepcopy as copy

class Var:
    def __init__(self,a=1,b=0,c=1):
        self.a=a#ax
        self.b=b#x+b
        self.c=c#x^c
    def __rmul__(self,k):
        return Var(self.a*k,self.b,self.c)
    def __mul__(self,k):
        return Var(self.a*k,self.b,self.c)
    def __truediv__(self,k):
        return Var(self.a/k,self.b,self.c)
    def __add__(self,k):
        return Var(self.a,self.b+k,self.c)
    def __radd__(self,k):
        return Var(self.a,self.b+k,self.c)
    def __sub__(self,k):
        return Var(self.a,self.b-k,self.c)
    def __neg__(self):
        return Var(self.a,self.b*-1,self.c)
    def __pow__(self,k):
        return Var(self.a,self.b,self.c*k)
    def __call__(self,x):
        if isinstance(self.a,Var):
            a=self.a(x)
        else:
            a=self.a
        if isinstance(self.b,Var):
            b=self.b(x)
        else:
            b=self.b
        if isinstance(self.c,Var):
            c=self.c(x)
        else:
            c=self.c
            
        y=a*x**c+b
        return y

class Movement:
    def __init__(self,formula):
        self.formula=formula
    def call(self,t):
        return self.formula(t)

from threading import Timer as _Timer
import time as _time

class anim:
    def __init__(self,function,start,duration,arg=[]):
        self._start=_time.time()+start
        self.func=function
        self._duration=duration
        self._end=self._start+self._duration
        self.arg=arg
    def __call__(self):
        now=_time.time()
        while(now<self._end):
            now=_time.time()
            dt=now-self._start
            self.func(*self.arg,dt/self._duration)

class animation:
    def __init__(self,function,start,duration):
        self.func=function
        self._start=start
        self.duration=duration
    def run(self,arg=[]):
        action=anim(self.func,self._start,self.duration,arg)
        _Timer(self._start,action).start()

class Progress:
    def __init__(self,s,e):
        self.s,self.e=s,e
    def __call__(self,i):
        return self.s+(self.e-self.s)*i