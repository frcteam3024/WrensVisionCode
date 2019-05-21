import numpy
import cv2
import math

#camra        
cam = cv2.VideoCapture(0)

class settings():
    #public
    width = int(cam.get(3))
    height = int(cam.get(4))
    edgeValue = 50
    skipSize = 100 # 100 = 1 * width
    lineY = [height // 2,height // 3,height // 3 * 2]#0 is top    #demonstration [height // 2,height // 3,height // 3 * 2]

class scan():
    #public
    bestPixal = [[0,0,0],[0,0,0]] #[nloop][y,x,value]
    #private
    nloop = 0 #0-1
    gValue = 0
    def main(self,nloop):
        self.nloop = nloop
        self.bestPixal[self.nloop] = 0,0,-255#reset y,x,value
        self.line()
        return 0
    
    def line(self):
        for lineY in settings.lineY:
            for i in range(settings.width):
                if findEdges.lineSkip[0] < i  < findEdges.lineSkip[1]:
                    i = findEdges.lineSkip[1]
                self.gValue = gValueF(lineY,i)
                if self.gValue > self.bestPixal[self.nloop][2]:
                    self.bestPixal[self.nloop] = lineY, i , self.gValue
        return 0
    
class findEdges():
    #public
    lineSkip = [0,0]#left,right
    sides = [[[0,0],[0,0],[0,0],[0,0],[0,0],0],
             [[0,0],[0,0],[0,0],[0,0],[0,0],0]] #[nloop][left,right,down,up,xcenter,found][y,x] found does no have [x,y]
    #private
    nloop = 0#0-1
    pointH = [0,0]#[y,x] and middle of rectangle
    pointV = [0,0]#[y,x]
    def main(self,nloop):
        self.nloop = nloop
        self.sides[self.nloop] = [[0,0],[0,0],[0,0],[0,0],[0,0],0]
        
        self.findH()
        self.setSkip()
        if self.sides[self.nloop][5] == 1:
            self.findV()
        return 0
    
    def findH(self):
        exitR = False
        exitL = False
        self.pointH[0] = scan.bestPixal[self.nloop][0]#y set to green point
        self.pointH[1] = scan.bestPixal[self.nloop][1]#x
        while exitR == False and gValueF(self.pointH[0],self.pointH[1]) > settings.edgeValue: #go right
            self.sides[self.nloop][1][0] = self.pointH[0]
            self.sides[self.nloop][1][1] = self.pointH[1]
            self.sides[self.nloop][5] = 1 #set found
            self.pointH[1] += 1
            if self.pointH[1] > settings.width - 1 or self.pointH[1] < 1:
                exitR = True
                
        self.pointH[0] = scan.bestPixal[self.nloop][0]#y set to green point
        self.pointH[1] = scan.bestPixal[self.nloop][1]#x
        while exitL == False and gValueF(self.pointH[0],self.pointH[1]) > settings.edgeValue: #go left
            self.sides[self.nloop][0][0] = self.pointH[0]
            self.sides[self.nloop][0][1] = self.pointH[1]
            self.sides[self.nloop][5] = 1 #set found
            self.pointH[1] -= 1
            if self.pointH[1] > settings.width - 1 or self.pointH[1] < 1:
                exitL = True
        return 0
    
    def findV(self):
        exitU = False
        exitD = False
        self.pointV[0] = self.pointH[0]
        self.pointV[1] = self.pointH[1]
        while exitU == False and gValueF(self.pointV[0],self.pointV[1]) > settings.edgeValue: # go down
            self.sides[self.nloop][2][0] = self.pointV[0]
            self.sides[self.nloop][2][1] = self.pointV[1]
            self.pointV[0] += 1
            if self.pointV[0] > settings.height - 1 or self.pointV[0] < 1:
                exitU = True

        self.pointV[0] = self.pointH[0]
        self.pointV[1] = self.pointH[1]
        while exitD == False and gValueF(self.pointV[0],self.pointV[1]) > settings.edgeValue: # go up
            self.sides[self.nloop][3][0] = self.pointV[0]
            self.sides[self.nloop][3][1] = self.pointV[1]
            self.pointV[0] -= 1
            if self.pointV[0] > settings.height - 1 or self.pointV[0] < 1:
                exitD = True
        return 0
    
    def setSkip(self):#and center
        boxWidth = self.sides[self.nloop][1][1] - self.sides[self.nloop][0][1]
        #set lineSkip
        self.lineSkip[0] = self.sides[self.nloop][0][1] - boxWidth * settings.skipSize / 100
        self.lineSkip[1] = self.sides[self.nloop][1][1] + boxWidth * settings.skipSize / 100
        if self.lineSkip[0] < 0:
            self.lineSkip[0] = 0
        if self.lineSkip[1] > settings.width - 1:
            self.lineSkip[1] = settings.width - 1
        #center pointH
        self.pointH[1] = self.sides[self.nloop][0][1] + boxWidth // 2
        self.sides[self.nloop][4][1] = self.pointH[1]
        self.sides[self.nloop][4][0] = self.pointH[0]
        return 0

class display():
    def main(self,frame,time):
        self.rectangle(frame)
        self.other(frame,time)
        return 0
    
    def rectangle(self,frame):
        for i in range(2):
            frame = cv2.circle(frame,(int(scan.bestPixal[i][1]),int(scan.bestPixal[i][0])),5,(0,0,255),-1)#x,y best green
            if findEdges.sides[i][5] == 1:
                frame = cv2.rectangle(frame,(int(findEdges.sides[i][0][1]),int(findEdges.sides[i][3][0])),(int(findEdges.sides[i][1][1]),int(findEdges.sides[i][2][0])),(255,0,255),3)#top-left,bottom-right
                frame = cv2.circle(frame,(int(findEdges.sides[i][0][1]),int(findEdges.sides[i][0][0])),5,(255,0,0),-1)#left
                frame = cv2.circle(frame,(int(findEdges.sides[i][1][1]),int(findEdges.sides[i][1][0])),5,(255,0,0),-1)#right
                frame = cv2.circle(frame,(int(findEdges.sides[i][2][1]),int(findEdges.sides[i][2][0])),5,(255,0,0),-1)#down
                frame = cv2.circle(frame,(int(findEdges.sides[i][3][1]),int(findEdges.sides[i][3][0])),5,(255,0,0),-1)#up
                frame = cv2.circle(frame,(int(findEdges.sides[i][4][1]),int(findEdges.sides[i][4][0])),5,(255,0,0),-1)#centerX
        return 0
    
    def other(self,frame,time):
        for i in settings.lineY:
            frame = cv2.circle(frame,(0,i),5,(0,255,0),-1)

        if cv2.getTickCount() % 50 == 0:
            print()
            print('  left    right   up      down    center   active')
            print(findEdges.sides[0])
            print(findEdges.sides[1])
            print('CycleTime =')
            print(time)
        return 0
    
#not in class for some reason
def gValueF(y,x):
    i = int(frame.item(int(y),int(x),1) - frame.item(int(y),int(x),0) / 2 - frame.item(int(y),int(x),2) / 2)#y,x
    return i



#setup classes
scan = scan()
findEdges = findEdges()
display = display()
settings = settings()


print('width', settings.width)
print('height', settings.height)


while(True):
    #Capture frame
    framebool, frame = cam.read()

    T1 = cv2.getTickCount()

    #loop twice
    for i in range(2):
        scan.main(i)
        findEdges.main(i)

    T2 = cv2.getTickCount()
    time = (T2 - T1)/ cv2.getTickFrequency()
    
    display.main(frame,time)

    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release the capture
cam.release()
cv2.destroyAllWindows()
