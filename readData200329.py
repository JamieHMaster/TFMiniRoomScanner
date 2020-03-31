##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
import serial, time
from math import *
from vpython import canvas, sphere, color, vector, arrow

window = canvas(title='3D Room Scan', width=1000, height=1000) 

serial_port = 'COM5'
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)
write_to_file_path = "output.txt"

output_file = open(write_to_file_path, "w+")
ser = serial.Serial(serial_port, baud_rate)

strengthMaxVaue = 10000

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
    def __init__(self, Dist, Strength, Pan, Tilt):
        self.Dist, self.Strength, self.Pan, self.Tilt = int(Dist), float(Strength), 90 - float(Pan), 90 - float(Tilt)
        print(self.Dist, self.Strength, self.Pan, self.Tilt)
        self.Xpos, self.Ypos, self.Zpos = 0, 0, 0
        self.pointColor = mapRanges(self.Strength, 0, strengthMaxVaue, 0, 256)
        self.red = self.pointColor/(256**2)
        self.green = (self.pointColor/256)%256
        self.blue = self.pointColor%256

    def calculateXpos(self):
        self.Xpos = self.Dist*sin(radians(self.Tilt))*sin(radians(self.Pan))

    def calculateYpos(self):
        self.Ypos = self.Dist*cos(radians(self.Tilt))

    def calculateZpos(self):
        self.Zpos = self.Dist*sin(radians(self.Tilt))*cos(radians(self.Pan))

    def addPoint(self):
        global lineToPoint
        self.calculateXpos()
        self.calculateYpos()
        self.calculateZpos()
        lineToPoint.axis=vector(self.Xpos, self.Ypos, self.Zpos)
        self.Pos = sphere(pos = vector(self.Xpos,self.Ypos,self.Zpos), radius = 0.2, color = vector(self.red,self.green,self.blue), canvas = window, make_trail=False)
        #print(vector(self.red,self.green,self.blue))

origin = sphere(pos = vector(0,0,0), radius = 3, color = color.green, canvas = window, make_trail=True)
Xaxis = arrow(pos=vector(0,0,0), axis=vector(100,0,0), shaftwidth=1, color=vector(1,0,0))
Yaxis = arrow(pos=vector(0,0,0), axis=vector(0,100,0), shaftwidth=1, color=vector(0,1,0))
Zaxis = arrow(pos=vector(0,0,0), axis=vector(0,0,100), shaftwidth=1, color=vector(0,0,1))
lineToPoint = arrow(pos=vector(0,0,0), axis=vector(0,0,0), shaftwidth=1, color=vector(0,1,1))

while True:
    line = ser.readline()
    line = str(line.decode("utf-8")) #ser.readline returns a binary, convert to string
    output_file.write(line)
    temp = line.split(" ")

    if temp[0].strip() == "DS":
        pointDist, PointTemp, PointStrength = temp[1], temp[2], temp[3]
    elif temp[0].strip() == "PT":
        PointPan, PointTilt = temp[1], temp[2]
        spheres.append(createPoints(pointDist, PointStrength, PointPan, PointTilt))
        spheres[-1].addPoint()