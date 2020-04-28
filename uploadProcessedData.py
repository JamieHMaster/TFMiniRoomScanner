##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
import serial, time, colorsys
from math import *
from vpython import canvas, sphere, color, vector, arrow, text, checkbox

window = canvas(title='3D Room Scan', width=600, height=600, background=color.white) 

spheres = []
pointDist = 100

def showDistance():
    hudShowStrength.checked = False
    for i in spheres:
        i.setColor("distance")

def showStrength():
    hudShowDist.checked = False
    for i in spheres:
        i.setColor("strength")

def HSLtoRGB(value, saturation, lightness, minimum, maximum):
    HUE = (value - minimum)/(maximum-minimum)*250 # 250 is the upper end of blue hue
    R = colorsys.hls_to_rgb(HUE/360, lightness/100, saturation/100)[0]
    G = colorsys.hls_to_rgb(HUE/360, lightness/100, saturation/100)[1]
    B = colorsys.hls_to_rgb(HUE/360, lightness/100, saturation/100)[2]
    print(value, minimum, maximum, HUE, saturation, lightness, R, G, B)
    return R, G, B

class createPoints():
    def __init__(self, X, Y, Z, RDist, GDist, BDist, RSTrength, GStrength, BStrength):
        global pointDist
        self.RGB = (0,0,0)
        self.Xpos, self.Ypos, self.Zpos = float(X), float(Y), float(Z)
        self.RDist, self.GDist, self.BDist, self.RSTrength, self.GStrength, self.BStrength = float(RDist), float(GDist), float(BDist), float(RSTrength), float(GStrength), float(BStrength)
        if sqrt(self.Xpos**2+self.Ypos**2+self.Zpos**2) > pointDist:
            pointDist = sqrt(self.Xpos**2+self.Ypos**2+self.Zpos**2)
            Xaxis.length = pointDist
            Yaxis.length = pointDist
            Zaxis.length = pointDist

    def setColor(self, colorBasedOn):
        if colorBasedOn == "distance":
            self.RGB = (self.RDist, self.GDist, self.BDist)
        elif colorBasedOn == "strength":
            self.RGB = (self.RSTrength, self.GStrength, self.BStrength)

    def addPoint(self):
        global lineToPoint
        lineToPoint.axis=vector(self.Xpos, self.Ypos, self.Zpos)
        self.Pos = sphere(pos = vector(self.Xpos,self.Ypos,self.Zpos), radius = 0.8, color = vector(self.RGB[0], self.RGB[1], self.RGB[2]), canvas = window, make_trail=False)
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

hudShowDist = checkbox(pos = window.caption_anchor, text = "Show distance", bind=showDistance)
hudShowStrength = checkbox(pos = window.caption_anchor, text = "Show Strength", bind=showStrength)
hudShowDist.checked = True
hudShowDist.disabled = True
hudShowStrength.disabled = True

def main(fileName):
    print(fileName)
    openFile = open(str(fileName), "r")
    while True:
        line = openFile.readline()
        print(line)
        if not line == "":
            temp = line.split(" ")
            spheres.append(createPoints(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8]))
            spheres[-1].addPoint()