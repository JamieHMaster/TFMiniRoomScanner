##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
import serial, time, colorsys
from math import *
from vpython import canvas, sphere, color, vector, arrow, text, wtext

window = canvas(title='3D Room Scan', width=1000, height=1000, background=color.white) 

serial_port = 'COM5'
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)
ser = serial.Serial(serial_port, baud_rate)

strengthMaxVaue = 10000
distMaxValue = 48000
longestDist = 100 # the furthest distance a point is from the origin. This controls the size of the arrows

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
        global pointDist
        self.Dist, self.Strength, self.Pan, self.Tilt = int(Dist)+5, float(Strength), 90 - float(Pan), 90 - float(Tilt)
        hudDist.text = " Distance: " + str(self.Dist)
        hudStrength.text = " Strength: " + str(self.Strength)
        hudPan.text = " Pan: " + str(90-self.Pan)
        hudTilt.text = " Tilt: " + str(90-self.Tilt)
        if self.Dist > pointDist:
            pointDist = self.Dist
            Xaxis.length = pointDist
            Yaxis.length = pointDist
            Zaxis.length = pointDist
        #print(self.Dist, self.Strength, self.Pan, self.Tilt)
        self.Xpos, self.Ypos, self.Zpos = 0, 0, 0
        self.pointColor = mapRanges(self.Dist, 0, strengthMaxVaue, 0, 140)
        self.pointColor = colorsys.hsv_to_rgb(self.pointColor,1,1)
        #print(self.pointColor)

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
        self.Pos = sphere(pos = vector(self.Xpos,self.Ypos,self.Zpos), radius = 0.8, color = vector(self.pointColor[0], self.pointColor[1], self.pointColor[2]), canvas = window, make_trail=False)
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

hudDist = wtext(pos = window.title_anchor, text = "Distance")
hudStrength = wtext(pos = window.title_anchor, text = "Strength")
hudPan = wtext(pos = window.title_anchor, text = "Pan")
hudTilt = wtext(pos = window.title_anchor, text = "Tilt")

onX50.length *= 2
onY50.length *= 2
onZ50.length *= 2
onX100.length *= 2
onY100.length *= 2
onZ100.length *= 2

onX50.height *= 2
onY50.height *= 2
onZ50.height *= 2
onX100.height *= 2
onY100.height *= 2
onZ100.height *= 2

def main(resolution, average, minPan, maxPan, minTilt, maxTilt, saveLocation):
    try:
        output_file = open(str(saveLocation), "w+")
    except:
        output_file = open("Output/output.txt", "w+")
    time.sleep(1)
    print(resolution, minPan, maxPan, minTilt, maxTilt)
    ser.write("<".encode())
    ser.write((resolution).encode())
    ser.write(">".encode())
    ser.write("<".encode())
    ser.write((average).encode())
    ser.write(">".encode())
    ser.write("<".encode())
    ser.write((minPan).encode())
    ser.write(">".encode())
    ser.write("<".encode())
    ser.write((maxPan).encode())
    ser.write(">".encode())
    ser.write("<".encode())
    ser.write((minTilt).encode())
    ser.write(">".encode())
    ser.write("<".encode())
    ser.write((maxTilt).encode())
    ser.write(">".encode())

    while True:
        line = ser.readline()
        line = str(line.decode("utf-8")) #ser.readline returns a binary, convert to string
        output_file.write(line)
        print(line)
        temp = line.split(" ")

        if temp[0].strip() == "DS":
            pointDist, PointTemp, PointStrength = temp[1], temp[2], temp[3]
        elif temp[0].strip() == "PT":
            PointPan, PointTilt = temp[1], temp[2]
            spheres.append(createPoints(pointDist, PointStrength, PointPan, PointTilt))
            spheres[-1].addPoint()