# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 18:28:13 2020

@author: Lumirevel
"""
#easings.net 참조함

import math

sqrt=math.sqrt
sin=math.sin
cos=math.cos
PI=math.pi

def easeInSine(x):
    return 1-cos((x*PI)/2)

def easeOutSine(x):
    return sin((x*PI)/2)

def easeInOutSine(x):
    return -(cos(PI*x)-1)/2

def easeInQuad(x):
    return x*x

def easeOutQuad(x):
    return 1-(1-x)*(1-x)

def easeInOutQuad(x):
    if x<0.5:
        return 2*x*x
    else:
        return 1-pow(-2*x+2,2)/2
        
def easeInCubic(x):
    return x*x*x
    
def easeOutCubic(x):
    return 1-pow(1-x,3)

def easeInOutCubic(x):
    if x<0.5:
        return 4*x*x*x
    else:
        return 1-pow(-2*x+2,3)/2
    
def easeInQuart(x):
    return x*x*x*x

def easeOutQuart(x):
    return 1-pow(1-x,4)

def easeInOutQuart(x):
    if x < 0.5:
        return 8*x*x*x*x
    else:
        return 1-pow(-2*x+2,4)/2
    
def easeInQuint(x):
    return x*x*x*x*x

def easeOutQuint(x):
    return 1-pow(1-x,5)

def easeInOutQuint(x):
    return  16*x*x*x*x*x if x<0.5 else 1-pow(-2*x+2,5)/2

def easeInExpo(x):
    return 0 if x == 0 else pow(2,10*x-10)

def easeOutExpo(x):
    return 1 if x == 1 else 1-pow(2,-10*x)

def easeInOutExpo(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    elif x < 0.5:
        return pow(2,20*x-10)/2
    else:
        return (2-pow(2,-20*x+10))/2
    
def easeInCirc(x):
    return 1-sqrt(1-pow(x,2))

def easeOutCirc(x):
    return sqrt(1-pow(x-1,2))

def easeInOutCirc(x):
    return (1-sqrt(1-pow(2*x,2)))/2 if x < 0.5 else (sqrt(1-pow(-2*x+2,2))+1)/2

def easeInBack(x):
    c1 = 1.70158
    c3 = c1 + 1
    return c3*x*x*x-c1*x*x

def easeOutBack(x):
    c1 = 1.70158
    c3 = c1 + 1
    return 1+c3*pow(x-1,3)+c1*pow(x-1,2)

def easeInOutBack(x):
    c1 = 1.70158
    c2 = c1*1.525
    return (pow(2*x,2)*((c2+1)*2*x-c2))/2 if x < 0.5 else (pow(2*x-2,2)*((c2+1)*(x*2-2)+c2)+2)/2

def easeInElastic(x):
    c4=(2*PI)/3
    return 0 if x == 0 else 1 if x == 1 else -pow(2,10*x-10)*sin((x*10-10.75)*c4)

def easeOutElastic(x):
    c4=(2*PI)/3
    return 0 if x == 0 else 1 if x == 1 else pow(2,-10*x)*sin((x*10-0.75)*c4)+1

def easeInOutElastic(x):
    c5=(2*PI)/4.5
    return 0 if x == 0 else 1 if x == 1 else -(pow(2,20*x-10)*sin((20*x-11.125)*c5))/2 if x < 0.5 else (pow(2,-20*x+10)*sin((20*x-11.125)*c5))/2+1

def easeInBounce(x):
    return 1-easeOutBounce(1-x)

def easeOutBounce(x):
    n1 = 7.5625
    d1 = 2.75

    if x < 1/d1:
        return n1*x*x
    elif x < 2/d1:
        x -= 1.5/d1
        return n1*x*x+0.75
    elif x < 2.5/d1:
        x -= 2.25/d1
        return n1*x*x+0.9375
    else:
        x -= 2.625/d1
        return n1*x*x+0.984375

def easeInOutBounce(x):
    return (1-easeOutBounce(1-2*x))/2 if x < 0.5 else (1+easeOutBounce(2*x-1))/2