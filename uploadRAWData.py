import time, colorsys
from math import *
from vpython import canvas, sphere, color, vector, arrow, text, wtext, checkbox

window = canvas(title='3D Room Scan', width=600, height=600, background=color.white) 

distMinValue = 100 # set the minimum distance the points have been from the sensor. This helps color in the dots at the end of the scan
distMaxValue = 100 # set the maximum distance the points have been from the sensor. This helps color in the dots at the end of the scan and to control the size of the axis arrows
strengthMinValue = 6500 # set the minimum strength the points have been from the sensor. This helps color in the dots at the end of the scan
strengthMaxValue = 6500 # set the maximum strength the points have been from the sensor. This helps color in the dots at the end of the scan

PointSize = 1.0

spheres = []

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
    def __init__(self, Dist, Temperature, Strength, Pan, Tilt):
        global distMinValue, distMaxValue, strengthMinValue, strengthMaxValue, PointSize
        self.Dist, self.Temp, self.Strength, self.Pan, self.Tilt = int(Dist)+5, float(Temperature), float(Strength), 90 - float(Pan), 90 - float(Tilt)
        self.pointSize = float(PointSize)
        hudDist.text = " Distance: " + str(self.Dist)
        hudStrength.text = " Strength: " + str(self.Strength)
        hudPan.text = " Pan: " + str(90-self.Pan)
        hudTilt.text = " Tilt: " + str(90-self.Tilt)
        if self.Dist < distMinValue:
            distMinValue = self.Dist
        if self.Dist > distMaxValue:
            distMaxValue = self.Dist
            Xaxis.length = distMaxValue
            Yaxis.length = distMaxValue
            Zaxis.length = distMaxValue
        if self.Strength < strengthMinValue:
            strengthMinValue = self.Strength
        if self.Strength > strengthMaxValue:
            strengthMaxValue = self.Strength
        #print(self.Dist, self.Strength, self.Pan, self.Tilt)
        self.Xpos, self.Ypos, self.Zpos = 0, 0, 0
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
        self.Pos = sphere(pos = vector(self.Xpos,self.Ypos,self.Zpos), radius = self.pointSize, color = vector(0,0,0), canvas = window, make_trail=False)
        #print(vector(self.red,self.green,self.blue))

    def setColor(self, showBasedOn):
        global distMinValue
        global distMaxValue

        if showBasedOn == "distance":
            self.RGBColor = HSLtoRGB(self.Dist, 100, 50, distMinValue, distMaxValue)
        elif showBasedOn == "strength":
            self.RGBColor = HSLtoRGB(self.Strength, 100, 50, strengthMinValue, strengthMaxValue)
        else:
            self.RGBColor = (0,0,0)

        self.Pos.color = vector(self.RGBColor[0], self.RGBColor[1], self.RGBColor[2])
    
    def getData(self):
        return str(self.Xpos) + " " + str(self.Ypos) + " " + str(self.Zpos) + " " + str(self.RGBColor[0]) + " " + str(self.RGBColor[1]) + " " + str(self.RGBColor[2]) + "\n"

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

hudDist = wtext(pos = window.caption_anchor, text = "Distance ")
hudStrength = wtext(pos = window.caption_anchor, text = "Strength ")
hudPan = wtext(pos = window.caption_anchor, text = "Pan ")
hudTilt = wtext(pos = window.caption_anchor, text = "Tilt ")
hudShowDist = checkbox(pos = window.caption_anchor, text = "Show distance", bind=showDistance)
hudShowStrength = checkbox(pos = window.caption_anchor, text = "Show Strength", bind=showStrength)
hudShowDist.checked = True
hudShowDist.disabled = True
hudShowStrength.disabled = True

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

def main(fileName):
    global PointSize
    print(fileName)
    openFile = open(str(fileName), "r")
    while True:
        line = openFile.readline()
        print(line)
        temp = line.split(" ")

        if temp[0].strip() == "DS":
            pointDist, PointTemp, PointStrength = temp[1], temp[2], temp[3]
        elif temp[0].strip() == "PT":
            PointPan, PointTilt = temp[1], temp[2]
            spheres.append(createPoints(pointDist, PointTemp, PointStrength, PointPan, PointTilt))
            spheres[-1].addPoint()
        elif temp[0].strip() == "Resolution":
            PointSize = float(temp[1])
            print(PointSize)
            time.sleep(5)
        elif temp[0].strip() == "done":
            break
    for i in spheres:
        i.setColor("distance")
    hudShowDist.disabled = False
    hudShowStrength.disabled = False
        