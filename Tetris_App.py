from graphics import *
from random import randrange
from Class_Button import *

class Object:

    def __init__(self,x,y,type):
        self.type=type
        self.direct=0
        self.__set(x,y)
        self.setPos()

    def __set(self,x,y):
        self.basic=[[]]
        if self.type==0:
           for i in range(-1,3):
              self.basic.append([x+i,y])
           self.basic=self.basic+[[x,y-1],[x,y+1],[x,y+2]]
           self.posList=[[1,2,3,4],[5,2,6,7]]*2
        else:
             xlist=[x-1,x,x+1];ylist=[y+1,y,y-1]
             for Y in ylist:
                for X in xlist:
                    self.basic.append([X,Y])
             if self.type==1:
                 self.posList=[[7,8,4,5]]*4
             elif self.type==2:
                 self.posList=[[4,5,6,1],[8,5,2,3],[9,4,5,6],[7,8,5,2]]
             elif self.type==3:
                 self.posList=[[4,5,6,3],[8,9,5,2],[7,4,5,6],[8,5,2,1]]
             elif self.type==4:
                 self.posList=[[7,8,5,6],[9,5,6,2]]*2
             elif self.type==5:
                 self.posList=[[4,5,6,2],[8,5,6,2],[8,4,5,6],[8,4,5,2]]
             elif self.type==6:
                 self.posList=[[8,9,4,5],[7,4,5,2]]*2

    def setPos(self):
        #기본 좌표나 방향이 바뀌었을 떄 객체의 직접적인 위치 갱신
        self.pos=[]
        for i in self.posList[self.direct]:
            self.pos.append(self.basic[i])

    def move(self,dx,dy):
        #기본 좌표 갱신
        #리스트 갱신 시 변수 할당 사용 불가능
        if self.__canMove(dx,dy):
            for i in range(1,len(self.basic)):
               point=self.basic[i]
               point[0]+=dx;point[1]+=dy
            self.setPos()

    def __canMove(self,dx,dy):
        #무브 메서드 조건 
        for (x,y) in self.pos:
            Nx=x+dx ;Ny=y+dy
            if Nx<1 or Nx>10:
                return False
            elif Ny<1:
                return False
        return True

    def getPos(self):
        pos=self.pos[:]
        return pos
    
    def getColor(self):
        return self.color

    def turn(self):
        #방향 갱신
        if self.direct==3:
            self.direct=0
        else:
            self.direct+=1
        self.setPos()
        dx=self.__checkTurn()
        return self.pos[:],dx

    def unturn(self,dx):
        if self.direct==0:
            self.direct==3
        else:
            self.direct-=1
        self.setPos()
        if dx:
          self.move(-dx,0)
        
    def __checkTurn(self):
        #턴 메서드에서 가로 위치 설정
         dx=0
         for (x,y) in self.pos:
             if x>10:
                 dx=10-x
             elif x<1:
                 dx=1-x
         if dx:
            self.move(dx,0)
         return dx
        
        
class Block:
    def __init__(self):
       t=randrange(7)
       self.types=['I','O','J','L','S','T','Z']
       self.type=self.types[t]
       x,y=self.__setCenter() 
       self.o=Object(x,y,t)
       self.color=color_rgb(randrange(0,256),randrange(0,256),randrange(0,256))

    def __setCenter(self):
        if self.type=='I':
            x=randrange(2,9)
        elif self.type=='O':
            x=randrange(2,11)
        else:
            x=randrange(2,10)
        y=22
        return x,y

    def move(self,dx,dy):
        self.o.move(dx,dy)
        return self.getPos()

    def getPos(self):
        pos=self.o.getPos();Npos=[]
        for (x,y) in pos:
            Npos.append([x,y,self.color])
        return Npos

    def turn(self):
        pos,dx= self.o.turn();Npos=[]
        for (x,y) in pos:
            Npos.append([x,y,self.color])
        return Npos,dx

    def unturn(self,dx):
        self.o.unturn(dx)
        

class Board:

    def __init__(self,level):
        self.Fill=[[[0,0]], [[0,0]], [[0,0]], [[0,0]], [[0,0]], [[0,0]], [[0,0]], [[0,0]], [[0,0]], [[0,0]], [[0,0]]]
        self.moving='';self.pos=[];self.shadow=[]
        #채워진 한줄 판단을 위해 필요
        self.YFill=[[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]
        self.score=0 ; self.Scores=[0,40,100,300,1200]
        self.level=level;self.__updateLevelUp();self.lines=0
       
    def __checkStop(self,dx,dy):
        stop=False
        #블록이 움직일 수 있는지 판단
        if dy:
            for (x,y,color) in self.pos[:]:
                Ny=y+dy
                for (y2,c) in self.Fill[x]:
                    if y2+1==Ny:
                        stop=True
                    elif y2==Ny:
                        dy+=1
                        stop=True
            self.pos=self.moving.move(0,dy)
                    
        if dx:
             for (x,y,color) in self.pos:
                  if dx==1 and y<21 and x+1 in self.YFill[y]:
                      dx=0
                  elif dx==-1 and y<21 and x-1 in self.YFill[y]:
                      dx=0
             if dx:
                self.pos=self.moving.move(dx,0);self.updateShadow()
        return stop 
         

    def __editFill(self):
        #같은 X좌표에서 Y좌표가 큰 것이 뒤에 있다.
        #멈춘 블록을 갱신 
        for (x,y,color) in self.newFill:
            self.Fill[x].append([y,color])
            if y<=20: 
              self.YFill[y].append(x)
        self.shadow=[]

    def dropAblock(self):
        #블럭 떨어뜨리는 메서드
        self.moving=Block()
        self.pos=self.moving.getPos()
        self.updateShadow()
        
    def __decideTurn(self):
        pos,dx=self.moving.turn()
        for (x,y,color) in pos:
            if y<21 and x in self.YFill[y]:
                self.moving.unturn(dx)
                return False,False
        self.pos=pos;self.updateShadow()
        for (x,y,color) in self.pos:
            for (y2,color) in self.Fill[x]:
                if y2+1==y:
                    return True,True
        return False,True
             
    def moveBlock(self,dx,dy):
        #블럭 움직이는 메서드
        self.pos=self.moving.getPos()
        stop=self.__checkStop(dx,dy)
        if stop:
            self.newFill=self.pos[:]
            self.moving=[] ;self.pos=[]
            self.__editFill()
            return 'Stop',[] 
        return self.pos,self.shadow

    def turnBlock(self):
        #돌아갈 수있는 지 판단하는 조건문 필요 
        stop,turn=self.__decideTurn()
        if stop:
            self.newFill=self.pos[:]
            self.moving=[] ;self.pos=[]
            self.__editFill()
            return 'Stop',[]
        elif turn:
            return self.pos,self.shadow
        else:return self.pos,''

    def updateShadow(self):
        dys=[];self.shadow=[]
        for (x,y,color) in self.pos:
            for (y2,color) in self.Fill[x]:
                if y2<y:
                    dy=y2-y+1;dys.append(dy)
        dy=max(dys)
        for (x,y,color) in self.pos:
            self.shadow.append([x,y+dy])

    def fall(self):
        #스페이스 사용 시 
        self.moving=[];self.newFill=[];color=self.pos[0][2]
        for (x,y) in self.shadow:
            self.newFill.append([x,y,color])
        self.pos=[]
        self.__editFill()

    def updateFill(self):
        removeY=[];levelUp=False
        y=0
        for xlist in self.YFill:
            if len(xlist)==11:
                removeY.append(y)
            y+=1
        if removeY:
            #self.Fill을 갱신하는 코드
             n=len(removeY); minY=min(removeY); maxY=max(removeY)
             if maxY-minY==3 and not (minY+2 in removeY) and minY+1 in removeY:ex=True
             else:ex=False
             Nfill=[[[0,0]]]
             for ylist in self.Fill[1:]:
                Nylist=[[0,0]]
                for (y,color) in ylist[1:]:
                    if y in removeY:pass
                    else:
                       if y<minY:
                           Nylist.append([y,color])
                       elif y>maxY:
                           Nylist.append([y-n,color])
                       elif minY<y<maxY:
                           if ex:
                               Nylist.append([y-2,color])
                           else:
                                Nylist.append([y-1,color])
                Nfill.append(Nylist)                   
             self.Fill=Nfill   
            #self.YFill을 갱신하는 코드
             NYfill=self.YFill[:minY]
             if maxY-minY+1!=n:
                 ys=[]
                 for i in range(minY+1,maxY):
                     if not i in removeY:ys.append(i)
                 for y in ys:
                     NYfill.append(self.YFill[y])
             for i in range(maxY+1,21):
                 NYfill.append(self.YFill[i])
             for x in range(n):
                 NYfill.append([0])
             self.YFill=NYfill
             #점수,레벨  갱신하는 코드
             levelUp=self.__setScore_Level(n)
             
        if len(self.Fill)!=11:print('error1')
        elif len(self.YFill)!=21 :
              print('error2',len(self.YFill))
              print(self.Fill,self.YFill)
              print(removeY)
        return self.Fill[:],self.score,levelUp

    def __setScore_Level(self,n):
        #updateFill()
        #라인,스코어,레벨 갱신
        levelUp=False;self.lines+=n
        if self.lines>=self.LevelUplines:
            self.level+=1
            self.lines=self.lines-self.LevelUplines
            self.__updateLevelUp()
            levelUp=True
        self.score+=self.Scores[n]*(self.level+1)
        return levelUp

    def __updateLevelUp(self):
            if 0<=self.level<10:
                self.LevelUplines=10
            elif 10<=self.level<=15:
                self.LevelUplines=20
            elif 15<self.level<=19:
                self.LevelUplines=30
            elif 20<=self.level<=28:
                self.LevelUplines=60

    def getScore(self):
        #전체 스코어 접근자
        return self.score
            
    def gameOver(self):
        if len(self.YFill[20])>1:
            return True
        return False
   
class Tetris_App:

    def __init__(self):
        self.interface=interface()
        self.Board=''
        self.level=0
        self.FPSs=[48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
        self.EasyMode=True

    def run(self):
        x=''
        while self.interface.wantToPlay(x,self.EasyMode) :
            x=self.playAgame()
            if x=='Qall':break
            score=self.Board.getScore()
            if score and x!='Replay':
              self.interface.checkRank(score)
        #모든 창 닫기
        self.interface.close()

    def playAgame(self):
        #레벨,속도 확정 
        self.level=self.interface.getLevel();self.interface.setLevel(self.level)
        self.Board=Board(self.level);self.FPS=self.FPSs[self.level]
        while not self.Board.gameOver(): 
            x=self.OneBlock()
            if x=='Quit':
                return 'Stop'
            elif x=='Replay' or x=='Qall':
                return x
            NewFill,score,LevelUp=self.Board.updateFill()
            if LevelUp:self.__updateLevel()
            self.interface.edit(NewFill,score,self.level,self.FPS)
        return 'End'

    def OneBlock(self):
        self.Board.dropAblock() 
        x,shadow=self.Board.moveBlock(0,-1)
        if x!='Stop':
          if not self.EasyMode:shadow=''
          self.interface.drawBlock(x,shadow)
        else:return ''
        #블록 낙하
        n=0
        while True:
            pos='' ;n+=1
            dx=0;dy=0;turn=False
            #플레이어와 상호작용
            key=self.interface.getKey()
            #퇴장,리플레이 or 이지모드
            if key=='Quit' or key=='Replay':
                stop,level=self.interface.checkStop(key)
                if level:self.interface.setLevel(level)
                if stop:return key
            elif key=='Qall':return key
            elif key=='Mode':
                if self.EasyMode:self.EasyMode=False
                else:self.EasyMode=True    

            #게임 내 상호작용
            elif key=='space':
                self.pos=self.Board.fall()
                break
            elif key:
               dx,dy,turn=self.movingBlock(key)
            #Block 일정한 낙하시기 일때
            if n%self.FPS==0:
                dy-=1
            if dx or dy:
                pos,shadow=self.Board.moveBlock(dx,dy)
                if pos=='Stop':break
            if turn:
                pos,shadow=self.Board.turnBlock()    
                if pos=='Stop':break
            #Borad객체로 부터 받은 위치로 인터페이스 갱신
            if not self.EasyMode:shadow=[]
            if pos:self.interface.drawBlock(pos,shadow)
            update(60)

            

    def movingBlock(self,key):
        dx=0;dy=0;turn=False
        if key=='Up' or key=='5':
             turn=True
        elif key=='Down' or key=='2':
             dy=-1
        elif key=='Right' or key=='3':
             dx=1
        elif key=='Left' or key=='1':
             dx=-1
        return dx,dy,turn

    def __updateLevel(self):
        self.level+=1
        self.FPS=self.FPSs[self.level]

       
class interface:

    def __init__(self):
        #랭크 저장 파일
        self.RankFileName='Tetris Rank.py'
        #시작 창 띄우기
        self.startWin=''
        self.__setStartWin()
        #메인창
        self.mainWin=''
        self.main=''
        #기록 기입창 
        self.RankWin=''
        #레벨 초기화 
        self.level=0
        
    def __setStartWin(self):
      if not self.startWin:
        #시작창 인터페이스
        self.startWin=GraphWin('READY WIN',970,600)
        name=Text(Point(400,40),'TETRIS');name.setSize(30);name.setStyle('bold');name.draw(self.startWin);name.setFill('red')
        info1=Text(Point(400,70),"Let's play Tetris") ;info1.setSize(15);info1.draw(self.startWin);info1.setFill('red')
        line=Line(Point(0,110),Point(800,110));line.setWidth(5);line.draw(self.startWin)
        line=Line(Point(400,110),Point(400,600));line.setWidth(4);line.draw(self.startWin)
        info2=Text(Point(200,140),'GAME KEYS');info2.setSize(17);info2.draw(self.startWin)
        info3=Text(Point(600,140),'GAME RANK');info3.setSize(17);info3.draw(self.startWin)
        c=200;w=60;y=200
        directKey=Polygon(Point(c-w/2,y),Point(c+w/2,y),Point(c+w/2,y+w),Point(c+w*3/2,y+w),Point(c+w*3/2,y+w*2),Point(c-w*3/2,y+w*2),Point(c-w*3/2,y+w),Point(c-w/2,y+w),Point(c-w/2,y))
        directKey.draw(self.startWin);directKey.setWidth(4);line=Line(Point(c-w/2,y+w),Point(c+w/2,y+w));line.setWidth(4);line.draw(self.startWin)
        line=Line(Point(c-w/2,y+w),Point(c-w/2,y+2*w));line.setWidth(4);line.draw(self.startWin)
        line=Line(Point(c+w/2,y+w),Point(c+w/2,y+2*w));line.setWidth(4);line.draw(self.startWin)
        line=Line(Point(c,y+8),Point(c,y+w-8));line.setArrow('first');line.setWidth(8);line.draw(self.startWin)
        line=Line(Point(c+w*3/2-8,y+w*3/2),Point(c+w/2+8,y+w*3/2));line.setArrow('first');line.setWidth(8);line.draw(self.startWin)
        line=Line(Point(c,y+w+8),Point(c,y+w*2-8));line.setArrow('last');line.setWidth(8);line.draw(self.startWin)
        line=Line(Point(c-w*3/2+8,y+w*3/2),Point(c-w/2-8,y+w*3/2));line.setWidth(8);line.setArrow('first');line.draw(self.startWin)
        info4=Text(Point(160,405),"Up Key :Change block's shape");info4.setSize(15);info4.draw(self.startWin)
        line=Line(Point(800,0),Point(800,600));line.draw(self.startWin);line.setWidth(4)
        info5=Text(Point(160,435),'Down Key :Drop block more fastly');info5.setSize(15);info5.draw(self.startWin)
        info6=Text(Point(135,465),'Right Key :Move block right');info6.setSize(15);info6.draw(self.startWin)
        info7=Text(Point(135,495),'Left Key :Move block left');info7.setSize(15);info7.draw(self.startWin)
        info8=Text(Point(50,365),'INFO');info8.setSize(18);info8.draw(self.startWin)
        c=Circle(Point(10,365),6);c.setFill('black');c.draw(self.startWin)
        startButton=Button(self.startWin,Point(725,50),110,60,'LEVEL:0\nSTART GAME');startButton.draw();startButton.activate()
        QuitButton=Button(self.startWin,Point(70,50),110,60,'CLOSE');QuitButton.draw();QuitButton.activate(); stopButton=Button(self.startWin,Point(60,560),100,50,'QUIT GAME'); stopButton.deactivate();stopButton.draw()
        #시작 창 버튼 리스트 
        self.Sbuttons=[startButton,QuitButton,stopButton]
        self.ranks=[];self.__setRank()
        #레벨 버튼
        self.levelButtons=[]
        for n in range(0,10):
            b=Button(self.startWin,Point(885,30+n*60),150,50,'{0} LEVEL'.format(n))
            b.activate();b.draw();self.levelButtons.append(b);b.transColor()
        self.levelButtons[0].deactivate()
            

    def __setRank(self):
        #시작 화면 랭킹 띄우기
        if self.ranks:
            for t in self.ranks:
                t.undraw()
            self.ranks=[]
        file=open(self.RankFileName,'r')
        ranks=file.readlines()[1:11]
        file.close()
        n=1 ;self.ranking=[]
        for x in ranks:
           name,score=x[:-1].split('/')
           self.ranking.append((name,score))
           t=Text(Point(600,200+40*(n-1)),'{0:^3}.     {1:^8}     {2:^8}'.format(n,name,score))
           t.setSize(15);t.draw(self.startWin);self.ranks.append(t)
           n+=1

    def __saveRank(self,rank,score):
        #모달 방식의 창
        #다른 인터페이스와 독립적 
        self.RankWin=GraphWin('ENTER SCORE!',400,300)
        name=Text(Point(200,40),'HIGH SCORE');name.setSize(25);name.setFill('blue');name.draw(self.RankWin)
        info1=Text(Point(200,110),'Congratulation, you are in Top 10.\nEnter your name to save it.');info1.setSize(15);info1.draw(self.RankWin)
        info2=Text(Point(150,160),'RANK :{0} / SCORE :{1}'.format(rank,score));info2.setFill('blue');info2.setSize(15);info2.draw(self.RankWin)
        self.PlayerName=Entry(Point(200,190),20);self.PlayerName.draw(self.RankWin);self.PlayerName.setSize(20)
        SaveButton=Button(self.RankWin,Point(340,260),100,50,'Save');SaveButton.draw();SaveButton.deactivate()
        QuitButton=Button(self.RankWin,Point(60,260),80,50,'Quit');QuitButton.draw();QuitButton.activate()
        while True:
            pt=self.RankWin.checkMouse()
            PlayerName=PlayerName=self.PlayerName.getText()
            if PlayerName:
                SaveButton.activate()
            else:
                SaveButton.deactivate()
            if pt:
                if SaveButton.Clicked(pt):
                    save=True
                    break
                elif QuitButton.Clicked(pt):
                    save=False
                    break
        if save:
            self.ranking.insert(rank-1,(PlayerName,score))
            file=open(self.RankFileName,'w')
            print('name/score',file=file)
            for (name,score) in self.ranking[:-1]:
                print('{0}/{1}'.format(name,score),file=file)
            file.close()
            self.__setRank()
        self.RankWin.close()

    def checkRank(self,Pscore):
        #랭크 확인 후 랭킹에 포함 시 수정 
        n=0;rank=0
        for (name,Rscore) in self.ranking:
            n+=1
            if '_' in name:
                rank=n;break
            elif int(Rscore)<=Pscore:
                rank=n;break
        if rank:self.__saveRank(rank,Pscore)
            
    def checkStop(self,x):
        #게임 도중 강제 종료
        if x[0]=='Q':key='Stop'
        elif x[0]=='R':key='Replay1'
        x=self.main.checkReplay(key)
        return x

    def wantToPlay(self,x,mode):
        #매번 새로운 게임을 시작하기 전 플레이어 리플레이 의사 묻기
        # 게임 도중 퇴장 또는 리플레이
        if x=='Stop':
            self.__closeMainWin()
            self.__setStartWin()
        if x=='Replay':
             self.__closeMainWin()
             self.__setMainWin(mode)
             return True
        #게임 오버
        if self.mainWin:
            x,self.level=self.main.checkReplay('Replay2');self.setLevel(self.level)
            if x==True:
                self.__closeMainWin()
                self.__setMainWin(mode)
                return x
            else:
                self.__closeMainWin()
                self.__setStartWin()
        #스타트 윈에서만 완전한 프로그램 종료      
        while True: 
            index=self.__checkStartWin()
            if index==0:
                self.__closeMainWin()
                self.__setMainWin(mode)
                return True
            elif index==1: 
                return False

    def __checkStartWin(self):
        #wantToPlay메서드에서 활용
        pt=self.startWin.checkMouse()
        if pt:
            for b in self.Sbuttons:
                if b.Clicked(pt):
                    return self.Sbuttons.index(b)
            for b in self.levelButtons:
                if b.Clicked(pt):
                    self.levelButtons[self.level].activate()
                    b.deactivate();self.level=self.levelButtons.index(b)
                    self.Sbuttons[0].setText('LEVEL:{0}\nSTART GAME'.format(self.level))
                    
        return ''
            
    def __setMainWin(self,mode):
        #메인 창 띄우기
        if not self.mainWin:
          self.main=Tetris_Win(mode)
          self.mainWin=self.main.getWin()
          self.Sbuttons[0].deactivate()
          self.Sbuttons[2].activate()

    def __closeMainWin(self):
        #메인 창 닫기
        if self.mainWin:
           self.main.undrawButtons()
           self.Sbuttons[0].activate();self.Sbuttons[2].deactivate()
           self.mainWin.close()
           self.mainWin=''

    def close(self):
        #모든 창 닫기(유저가 게임 종료를 원할 때)
        if self.startWin:
            self.startWin.close()
        if self.mainWin:
            self.mainWin.close()
           
    def getKey(self):
        #모달방식X
        if self.mainWin:
            key=self.mainWin.checkKey() ;pt=self.mainWin.checkMouse()
            if key:
                return key
            elif pt:
                return self.main.checkQuit(pt)
            
        if self.startWin:
            pt=self.startWin.checkMouse()
            if pt and self.Sbuttons[1].Clicked(pt):
                self.startWin.close();self.startWin=''
            if pt and self.Sbuttons[2].Clicked(pt):
                return 'Qall'

    def getLevel(self):
        return self.level

    def setLevel(self,level):
        for b in self.levelButtons:
            b.activate()
        self.levelButtons[level].deactivate();self.level=level
        self.Sbuttons[0].setText('LEVEL:{0}\nSTART GAME'.format(self.level))
        self.main.setLevel(level)


#----------------------------------------------------------------------------------------------------------------------------------
    #원 블록 후 메인 창 수정 메서드(주로 self.main 메서드에 넘김)
    def drawBlock(self,points,shadow):
            self.main.draw(points,shadow)

    def edit(self,newFill,score,level,FPS):
        points=[];x=1;self.level=level
        for ylist in newFill[1:]:
            for (y,color) in ylist[1:]:
                points.append([x,y,color])
            x+=1
        self.main.edit(points,score,level,FPS)
                       

class Tetris_Win:

    def __init__(self,mode):
        self.win=GraphWin('TETRIS PLAYING...',700,850,autoflush=False)
        self.win.setCoords(-4,-2,10,20);self.EasyMode=mode
        rect=Rectangle(Point(-4,20),Point(-0.05,17));rect.setOutline('red');rect.setFill('red');rect.draw(self.win)
        line=Line(Point(0,20),Point(0,0));line.setWidth(5);line.draw(self.win)
        line=Line(Point(0,0),Point(10,0));line.setWidth(5);line.draw(self.win)
        name=Text(Point(-2,18.5),'TETRIS\nPLAY');name.setSize(30);name.setStyle('bold');name.setFill('blue');name.draw(self.win)
        replayButton=Button(self.win,Point(-1,-1),1.4,1.2,'Replay');replayButton.draw();replayButton.activate()
        QuitButton=Button(self.win,Point(-3,-1),1.4,1.2,'Quit');QuitButton.draw();QuitButton.activate()
        if mode==True:t1='OFF';t2='ON'
        else:t1='ON';t2='OFF'
        easyButton=Button(self.win,Point(-2,7.5),3,1,t1);easyButton.draw()
        rect=Rectangle(Point(-3.5,9.75),Point(-0.5,8.25));rect.draw(self.win);rect.setFill('Blue')
        self.Mode=Text(Point(-2,9),'EASY MODE\n{0}!'.format(t2));self.Mode.setSize(15);self.Mode.setFill('white');self.Mode.draw(self.win)
        for x in range(11):
            line=Line(Point(x,0),Point(x,20));line.setWidth(1);line.draw(self.win)
        for y in range(21):
            line=Line(Point(0,y),Point(10,y));line.setWidth(1);line.draw(self.win)
        rect=Rectangle(Point(-3.5,16.2),Point(-0.5,13.7));rect.setWidth(3);rect.draw(self.win)
        self.score=Text(Point(-2,14.4),'0');self.score.setSize(22);self.score.draw(self.win);rect=Rectangle(Point(-3.5,16.2),Point(-0.5,15));rect.setFill('blue');rect.draw(self.win);info1=Text(Point(-2,15.6),'SCORE');info1.setSize(22);info1.setFill('White');info1.draw(self.win)
        rect=Rectangle(Point(-3.5,13),Point(-0.5,10.5));rect.setWidth(3);rect.draw(self.win);rect=Rectangle(Point(-3.5,13),Point(-0.5,11.8));rect.setFill('Blue');rect.draw(self.win);info2=Text(Point(-2,12.4),'LEVEL');info2.setSize(22);info2.setFill('White');info2.draw(self.win)
        self.level=Text(Point(-2,11.2),'00');self.level.setSize(22);self.level.draw(self.win)
        self.buttons=[replayButton,QuitButton,easyButton]
        self.LevelButtons=[]
        for n in range(10):
            if n<5:x=n*2+1;y=6
            else:x=(n-5)*2+1;y=4
            b=Button(self.win,Point(x,y),2,2,'LEVEL\n{0}'.format(n));self.LevelButtons.append(b);b.transColor()
        self.FPS=Text(Point(9.3,-1.5),'FPS ').draw(self.win)
        self.blocks=[];self.shadows=[]
        self.Fill=[];self.Level=0
        
    def getWin(self):
        return self.win

    def checkQuit(self,pt):
        if self.buttons[0].Clicked(pt):
            return 'Replay'
        elif self.buttons[1].Clicked(pt):
            return 'Quit'
        elif self.buttons[2].Clicked(pt):
            if not self.EasyMode:t='OFF';t2='ON';self.EasyMode=True
            else:t='ON';t2='OFF';self.EasyMode=False
            self.buttons[2].setText(t)
            self.Mode.setText('EASY MODE\n{0}!'.format(t2))
            return 'Mode'
        else:
            return False
    
    def draw(self,points,shadow):
        if self.blocks:
            for block in self.blocks:
                block.undraw()
                self.blocks=[]
        if self.shadows:
            for s in self.shadows:
                s.undraw()
                self.shadows=[]
        for (x,y,color) in points:
            block=Rectangle(Point(x,y),Point(x-1,y-1))
            block.draw(self.win) ;block.setFill(color)
            self.blocks.append(block)
        if shadow:    
           for (x,y) in shadow:
               s=Rectangle(Point(x,y),Point(x-1,y-1))
               s.draw(self.win);s.setWidth(5);s.setOutline('red')
               self.shadows.append(s)

    def edit(self,points,score,level,FPS):
        if self.Fill:
            for i in self.Fill:
                i.undraw()
        for (x,y,color) in points:
            block=Rectangle(Point(x,y),Point(x-1,y-1)); block.setFill(color)
            block.draw(self.win);self.Fill.append(block)
        self.FPS.setText('FPS {0}'.format(FPS))

        self.score.setText(score)
        self.level.setText(level);self.Level=level

    def undrawButtons(self):
        for b in self.buttons:
            b.undraw()

    def setLevel(self,level):
        self.level.setText(level)
        self.Level=level

    def checkReplay(self,w):
        if w=='Stop':
            t1='Are You Really Want To Quit?';t2="";t3='Continue'
        elif w=='Replay1':
            t1='Do you want to replay?';t2="You Can't Save Score If You Clicked\n Replay Button.";t3='Continue'
        elif w=='Replay2':
            t1='Do you want to replay?';t2='Or you get back to startWin.';t3='Quit'
        Rect=Rectangle(Point(1,7),Point(9,13)); Rect.setFill('blue');Rect.draw(self.win)
        info=Text(Point(5,12),t1);info.setSize(22);info.setFill('White');info.draw(self.win)
        info1=Text(Point(5,10.8),t2);info1.setSize(14);info1.setFill('White');info1.draw(self.win)
        yes=Cbutton(self.win,Point(3.5,8.5),1,'YES');no=Cbutton(self.win,Point(6.5,8.5),1,t3);yes.draw();no.draw();yes.activate();no.activate()
        yes.setTextSize(13);no.setTextSize(13)
        if w[0]=='R':
            for b in self.LevelButtons:
               b.activate();b.draw()
            self.LevelButtons[self.Level].deactivate();Level=self.Level
            
        for i in self.buttons:
            i.deactivate()
        while True:
            pt=self.win.getMouse()
            if yes.Clicked(pt):
                op=True
                break
            elif no.Clicked(pt):
                op=False
                break
            elif w[0]=='R':
                for b in self.LevelButtons:
                    if b.Clicked(pt):
                        n=self.LevelButtons.index(b)
                        self.LevelButtons[Level].activate();self.LevelButtons[n].deactivate();Level=n
        Rect.undraw();info.undraw();info1.undraw();yes.undraw();no.undraw()
        for i in self.buttons:
            i.activate()
        for b in self.LevelButtons:
            b.undraw()
        if op and w[0]=='R':self.Level=Level
        return op,self.Level
                
                
        
        

if __name__=='__main__':                
    Tetris_App().run()
            
        

    
                
        
        
        







        
    
        

        
        
        
