from UI import *
from vector import vector
pygame.init()

#메인 창
class Window:
    def __init__(self,width=700,height=700):
        self.window_size=size=[width,height]
        self.screen=pygame.display.set_mode(size)
        self.bgcolor=(30,30,30)
        
        self.scene=[]
        self.sceneNum=None
        
        self.SPACE=False
        self.CLICK=False
        self.to=(0,0)
        self.done=False
        
        self.isflip=False
        self.init=True
        
    #게임을 창 중앙에 원점이 오도록 구현함
    #그런데 창에 띄울 때는 좌상단을 원점으로 한 좌표를 입력해야함
    #그래서 두 좌표 시스템을 변화해주는 pos2scr과 scr2pos 함수를 만듦
    def pos2scr(self,pos):#게임 좌표->화면 좌표
        x,y=pos
        window_center=vector(self.window_size)/2#맵 크기
        scrVec=vector(x,-y)+window_center
        return list(scrVec.quant())

    def scr2pos(self,scr):#화면 좌표->게임 좌표
        x,y=scr
        dx,dy=vector(self.window_size)/2#맵 크기
        return vector(x-dx,dy-y)
    
    #convert#화면에 띄울 때 사용하는 함수
    def drawRast(self,img,pos):#불러온 사진, 텍스트
        if not self.isflip:
            self.screen.fill(self.bgcolor)
        self.isflip=True
        rect=img.get_rect()
        rect.center=tuple(self.pos2scr(pos))
        self.screen.blit(img,rect)
        
    def drawBall(self,color,radius,pos):#원
        if not self.isflip:
            self.screen.fill(self.bgcolor)
        self.isflip=True
        x,y=pos
        width,height=self.window_size#맵 크기
        
        center=self.pos2scr(pos)#좌표 변환 중
        
        pygame.draw.circle(self.screen,color,center,radius,0)
        
    def drawRect(self,color,size,pos,angle):#다각형
        if not self.isflip:
            self.screen.fill(self.bgcolor)
        self.isflip=True
        #좌표 변환 전
        row,col = size/2#row=가로 길이 반,col=세로 길이 반
        
        a = pos + vector(-row,col).rotate(angle)#왼쪽 상단 모서리(회전 고려)
        b = pos + vector(-row,-col).rotate(angle)#왼쪽 하단 모서리(회전 고려)
        c = pos + vector(row,-col).rotate(angle)#오른쪽 하단 모서리(회전 고려)
        d = pos + vector(row,col).rotate(angle)#오른쪽 상단 모서리(회전 고려)
        
        #좌표 변환 중
        ap = self.pos2scr(a)
        bp = self.pos2scr(b)
        cp = self.pos2scr(c)
        dp = self.pos2scr(d)
        
        pygame.draw.polygon(self.screen,color,[ap,bp,cp,dp])
        
    #장면 추가
    def addscene(self,scene):
        self.scene.append(scene)
        if self.sceneNum == None:
            self.sceneNum=0
    
    #장면 바꾸기
    def scene(self,sceneNum):
        self.sceneNum=sceneNum
    
    #메인 과정   
    def main(self):
        while not self.done:#동작중
            #이벤트
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    self.done=True
                    
                elif ev.type==pygame.MOUSEBUTTONDOWN:
                    self.CLICK=True#마우스 클릭여부 업데이트
                    if self.scene:
                        self.scene[self.sceneNum].mousePressEvent(self)
                    
                elif ev.type==pygame.MOUSEMOTION:
                    self.to=self.scr2pos(ev.pos)#마우스 위치 업데이트
                    if self.scene:
                        self.scene[self.sceneNum].mouseMoveEvent(self)
                    
                elif ev.type==pygame.MOUSEBUTTONUP:
                    self.CLICK=False#마우스 클릭여부 업데이트
                    if self.scene:
                        self.scene[self.sceneNum].mouseReleaseEvent(self)
            
            #화면
            if self.scene:
                self.scene[self.sceneNum].main(self)
            if self.isflip:
                pygame.display.flip()
            self.isflip=False
        
        pygame.quit()#종료

class Movie:
    def __init__(self):
        self.zip=Zip()
    
    def mousePressEvent(self,window):
        pass
        
    def mouseMoveEvent(self,window):
        pass
            
    def mouseReleaseEvent(self,window):
        pass
    
    def main(self,window):
        pass