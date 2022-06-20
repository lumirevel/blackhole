# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 00:08:32 2021

@author: Lumirevel
"""
from vector import vector
class matrix(tuple):
    def __new__(cls,*arg):#벡터 생성
        v=[]
        for xi in arg:
            v.append(vector(*xi))
        return tuple.__new__(cls,v)
    
    def __rmul__(self,x):#x*self#실수배
        mat=[]
        for yi in self:
            mat.append(x*yi)
        return matrix(*mat)
        
    def __truediv__(self,y):#실수배(나눗셈)
        mat=[]
        for xi in self:
            mat.append(xi/y)
        return matrix(*mat)
    
    def __floordiv__(self,y):
        mat=[]
        for xi in self:
            mat.append(xi//y)
        return matrix(*mat)
    
    def __mul__(self,b):#self*y
        if isinstance(b,matrix):#내적
            mat=[]
            B=b
            for ai_ in self:
                cij=[]
                for b_j in B.T:
                    cij.append(ai_*b_j)
                mat.append(cij)
            return matrix(*mat)
        elif isinstance(b,vector):
            return (self*matrix(b).T).T[0]
        else:#실수배
            mat=[]
            for ai in self:
                mat.append(b*ai)
            return matrix(*mat)
    
    def __add__(self,y):#두 벡터의 합
        mat=[]
        for i,xi in enumerate(self):
            mat.append(xi+y[i])
        return vector(*mat)
    
    def __sub__(self,y):#두 벡터의 차
        mat=[]
        for i,xi in enumerate(self):
            mat.append(xi-y[i])
        return matrix(*mat)
    
    def __neg__(self):#역벡터
        mat=[]
        for xi in self:
            mat.append(-xi)
        return matrix(*mat)
    
    @property
    def T(self):
        mat=[]
        x0=self[0]
        for j,x0j in enumerate(x0):
            cell=[]
            for xi in self:
                cell.append(xi[j])
            mat.append(vector(cell))
        return matrix(*mat)#크기는 유지됨