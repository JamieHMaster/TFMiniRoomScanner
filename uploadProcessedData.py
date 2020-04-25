##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
import serial, time, colorsys
from math import *
from vpython import canvas, sphere, color, vector, arrow, text

window = canvas(title='3D Room Scan', width=1000, height=1000, background=color.white) 

strengthMaxVaue = 10000
distMaxValue = 48000
pointDist = 100

spheres = []
pointDist = 0
PointStrength = 0
PointTemp = 0
PointPan = 0
PointTilt = 0

def mapRanges(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class createPoints():
    def __init__(self, X, Y, Z, R, G, B):
        global pointDist
        print(float(X), float(Y), float(Z), R, G, B)
        self.Xpos, self.Ypos, self.Zpos = float(X), float(Y), float(Z)
        self.R, self.G, self.B = float(R), float(G), float(B)
        if sqrt(self.Xpos**2+self.Ypos**2+self.Zpos**2) > pointDist:
            pointDist = sqrt(self.Xpos**2+self.Ypos**2+self.Zpos**2)
            Xaxis.length = pointDist
            Yaxis.length = pointDist
            Zaxis.length = pointDist

    def addPoint(self):
        global lineToPoint
        lineToPoint.axis=vector(self.Xpos, self.Ypos, self.Zpos)
        self.Pos = sphere(pos = vector(self.Xpos,self.Ypos,self.Zpos), radius = 0.8, color = vector(self.R, self.G, self.B), canvas = window, make_trail=False)
        #print(vector(self.red,self.green,self.blue))

origin = sphere(pos = vector(0,0,0), radius = 3, color = color.green, canvas = window, make_trail=True)
Xaxis = arrow(pos=vector(0,0,0), axis=vector(100,0,0), shaftwidth=1, color=vector(1,0,0))
Yaxis = arrow(pos=vector(0,0,0), axis=vector(0,100,0), shaftwidth=1, color=vector(0,1,0))
Zaxis = arrow(pos=vector(0,0,0), axis=vector(0,0,100), shaftwidth=1, color=vector(0,0,1))
onX50 = text(text="50cm", align='center', color=vector(1,0,0), pos=vector(50,2,0))
onY50 = text(text="50cm", align='center', color=vector(0,1,0), pos=vector(4,50,0))
onZ50 = text(text="50cm", align='center', color=vector(0,0,1), pos=vector(0,2,50))
onX100 = text(text="100cm", align='center', color=vector(1,0,0), pos=vector(100,2,0))
onY100 = text(text="100cm", align='center', color=vector(0,1,0), pos=vector(4,100,0))
onZ100 = text(text="100cm", align='center', color=vector(0,0,1), pos=vector(0,2,100))
lineToPoint = arrow(pos=vector(0,0,0), axis=vector(0,0,0), shaftwidth=1, color=vector(0,1,1))

def main(fileName):
    print(fileName)
    openFile = open(str(fileName), "r")
    while True:
        line = openFile.readline()
        print(line)
        temp = line.split(" ")
        spheres.append(createPoints(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]))
        spheres[-1].addPoint()