from graphics import *
class Button:
   def __init__(self,win,center,width,height,label):
      self.win=win
      w=width/2
      h=height/2
      x=center.getX()
      y=center.getY()
      self.p1=Point(x+w,y+h)
      self.p2=Point(x-w,y-h)

      self.rect=Rectangle(self.p1,self.p2)
      self.rect.setWidth(3)

      self.label=Text(center,label)
      self.Text=label

      self.background='white'
      self.off='darkgray'
      self.rect.setFill(self.background)
      self.active=True

   def draw(self):
      self.rect.draw(self.win);self.label.draw(self.win)
      

   def Clicked(self,point):
     if self.active: 
       x=point.getX()
       y=point.getY()
       if self.p2.getX()<=x<=self.p1.getX() and self.p2.getY()<=y<=self.p1.getY():
         return True
       else:
         return False

   def activate(self):
      self.rect.setFill(self.background)
      self.active=True

   def deactivate(self):
      self.rect.setFill(self.off)
      self.active=False

   def undraw(self):
      self.rect.undraw()
      self.label.undraw()

   def setText(self,text):
       self.label.setText(text)
       self.Text=text

   def getText(self):
      return self.Text

   def transColor(self):
      self.background='darkgray'
      self.off='white'
      if self.activate:self.rect.setFill(self.background)
      else:self.rect.setFill(self.off)
      

#-------------------------------------------------------------------------------
class Cbutton:
   def __init__(self,win,center,radius,label):
      self.win=win
      self.x=center.getX()
      self.y=center.getY()
      self.radius=float(radius)
      
      self.cir=Circle(center,radius)

      self.label=Text(center,label)

      self.background='white'
      self.off='darkgray'
      self.cir.setFill(self.background)
      self.active=True

   def Clicked(self,point):
     if self.active: 
       x=point.getX()
       y=point.getY()
       from math import sqrt
       k=sqrt((self.x-x)**2+(self.y-y)**2)
       if k<=self.radius:
         return True
       else:
         return False

   def draw(self):
      self.cir.draw(self.win);self.label.draw(self.win)
      

   def activate(self):
      self.cir.setFill(self.background)
      self.active=True

   def deactivate(self):
      self.cir.setFill(self.off)
      self.active=False

   def undraw(self):
      self.cir.undraw()
      self.label.undraw()

   def setText(self,text):
       self.label.setText(text)

   def setWidth(self,wid):
      self.cir.setWidth(wid)

   def setOutline(self,color):
      self.cir.setOutline(color)

   def setTextSize(self,size):
      self.label.setSize(size)

