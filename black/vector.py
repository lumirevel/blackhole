import math#made by lumirevel

#연산용
class vector(tuple):#벡터 연산용
    def __new__(cls,*arg):#벡터 생성
        if len(arg)==1:
            if isinstance(arg[0],int) or isinstance(arg[0],float):
                return tuple.__new__(cls,arg)
            else:
                return tuple.__new__(cls,arg[0])
        else:
            return tuple.__new__(cls,arg)
    
    def __abs__(self):#벡터의 크기
        scalar=0
        for xi in self:
            scalar+=xi**2
        return math.sqrt(scalar)#l2공간
    
    def __mod__(self,q):
        vec=[]
        for xi in self:
            vec.append(xi%q)
        return vector(*vec)
    
    def quant(self):#quantization
        vec=[]
        for xi in self:
            vec.append(int(xi))
        return vector(*vec)
    
    def __rmul__(self,x):#x*self#실수배
        vec=[]
        for yi in self:
            vec.append(x*yi)
        return vector(*vec)
        
    def __truediv__(self,y):#실수배(나눗셈)
        vec=[]
        for xi in self:
            vec.append(xi/y)
        return vector(*vec)
    
    def __floordiv__(self,y):
        vec=[]
        for xi in self:
            vec.append(xi//y)
        return vector(*vec)
    
    def __mul__(self,y):#self*y
        if isinstance(y,vector):#내적
            scalar=0
            for i,xi in enumerate(self):
                scalar+=xi*y[i]
            return scalar
        
        else:#실수배
            vec=[]
            for xi in self:
                vec.append(y*xi)
            return vector(*vec)
        
    def cross_abs(self,b):#외적의 크기(오른손 좌표계)
        '''
        vector->scalar
        
        외적의 크기(오른손 좌표계)
        '''
        ax,ay=self
        bx,by=b
        return ax*by-ay*bx
    
    def __add__(self,y):#두 벡터의 합
        vec=[]
        for i,xi in enumerate(self):
            vec.append(xi+y[i])
        return vector(*vec)
    
    def __sub__(self,y):#두 벡터의 차
        vec=[]
        for i,xi in enumerate(self):
            vec.append(xi-y[i])
        return vector(*vec)
    
    def __neg__(self):#역벡터
        vec=[]
        for xi in self:
            vec.append(-xi)
        return vector(*vec)
    
    @property
    def x(self):#단위벡터
        return self[0]
    
    @property
    def y(self):#단위벡터
        if len(self)>=2:
            return self[1]
        else:
            return 0
    
    @property
    def z(self):#단위벡터
        if len(self)>=3:
            return self[2]
        else:
            return 0
        
    @property
    def unit(self):#단위벡터
        if not abs(self)==0:
            return self/abs(self)
        else:#0벡터이면
            return self
    
    @property    
    def n(self):#법선 벡터(90도 회전)
        '''
        2D
        
        None->vector
        
        법선 벡터 출력
        크기는 유지(90도 회전)
        '''
        ux,uy=self
        return vector(-uy,ux)#크기는 유지됨
    
    def rotate(self,angle):#회전(입력 단위:도)
        '''
        2D
        
        angle(단위: 도)->vector
        
        입력한 값(단위: 도)만큼 회전한 벡터를 출력
        '''
        theta=math.pi/180*angle#호도법(단위:라디안)
        
        Rx=vector(math.cos(theta),-math.sin(theta))
        Ry=vector(math.sin(theta),math.cos(theta))
        
        return vector(Rx*self,Ry*self)#회전한 벡터
    
    def cmm(n1,p1,n2,p2):#cross-multiplication-method#두 직선 방정식 교점
        '''
        두 직선의 교점의 좌표를 구하는 함수
        cross-multiplication-method 사용
        
        2D
        
        n1=첫번째 직선방정식의 법선 벡터
        p1=첫번째 직선방정식이 지나는 한 점
        n2=두번째 직선방정식의 법선 벡터
        p2=두번째 직선방정식이 지나는 한 점
        '''
        #ax+by+c=0꼴의 직선 방정식을 만드는 과정
        a1,b1=n1#벡터 n1 성분화
        a2,b2=n2#벡터 n2 성분화
        
        a=vector(a1,a2)
        b=vector(b1,b2)
        c=vector(-n1*p1,-n2*p2)
        
        x=b.cross_abs(c)/a.cross_abs(b)
        y=c.cross_abs(a)/a.cross_abs(b)
        return vector(x,y)#좌표를 벡터로 나타냄
    
    def signed_d(n1,p1,p):#점 직선 거리 공식을 응용함
        '''
        2D
        
        점 직선 거리 공식의 분자에
        절댓값을 씌우지 않음
        
        n1=직선의 법선 벡터
        p1=직선이 지나는 한점
        
        p=직선과 거리를 구하려는 점
        '''
        return n1.unit*(p-p1)
    
    def theta(self):
        unit=self.unit
        x=unit[0]
        y=unit[1]
        if y>0:
            if x>=0:#1
                return math.asin(y)
            else:#2
                return math.acos(x)
        else:
            if x<0:#3
                return -math.acos(x)
            else:#4
                return math.asin(y) % math.tau