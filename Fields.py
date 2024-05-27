#libraries
import numpy as np # type: ignore
import math as m

#magnetic permuability of free space
MU = 4*m.pi*10**-7

class RectCoil:
    # Initializes the array of wire elements and if no elements are provided it initializes an empty array
    def __init__(self, _x, _y, _z, _w, _dia):
        self.elements = []
        self.current = 98000 * m.pow(_dia, 1.27)
        for z in range(int(-(_z/_dia-1)/2), int((_z/_dia-1)/2)):
            for n in range(int(_w/_dia-1)):
                self.elements.append(Wire(_x+(n+1)*_dia, [0, _y+(n+0.5)*_dia, -(z+0.5)*_dia], [0, 0], self.current))
                self.elements.append(Wire(_y+(n+1)*_dia, [_x+(n+0.5)*_dia, 0, -(z+0.5)*_dia], [270, 0], self.current))
                self.elements.append(Wire(_x+(n+1)*_dia, [0, -_y+(n+0.5)*_dia, -(z+0.5)*_dia], [180, 0], self.current))
                self.elements.append(Wire(_y+(n+1)*_dia, [-_x+(n+0.5)*_dia, 0, -(z+0.5)*_dia], [90, 0], self.current))
        self.dim = [_x+_w*2, _y+_w*2, _z]
    #gets the field strength of a point around the coil
    def get(self, point):
        fieldStrength = [0,0,0]
        for i in range(len(self.elements)):
            fieldStrength =  np.add(fieldStrength, self.elements[i].get(point))
        return fieldStrength

class Coil:
    #initializes the array of wire elements and if no elements are provided it initializes an empty array
    def __init__(self, _elements = []):
        self.elements = _elements
    #adds element to the coil
    def addElement(self, element):
        self.elements.append(element)
        return
    #gets the field strength of a point around the coil
    def get(self, point):
        fieldStrength = [0,0,0]
        for i in range(len(self.elements)):
            fieldStrength =  np.add(fieldStrength, self.elements[i].get(point))
        return fieldStrength
        
class Wire:
    #initializes all the parameters of the straight wire
    def __init__(self, _length, _location, _orientation, _current):
        self.length = _length
        self.location = _location
        #Forward orentation or sin(theta), cos(theta)
        self.fOrientation = [[m.sin(_orientation[0]*m.pi/180), m.cos(_orientation[0]*m.pi/180)], [m.sin(_orientation[1]*m.pi/180), m.cos(_orientation[1]*m.pi/180)]]
        #Reverse orientation or sin(-theta), cos(-theta)
        self.rOrientation = [[m.sin(-_orientation[0]*m.pi/180), m.cos(-_orientation[0]*m.pi/180)], [m.sin(-_orientation[1]*m.pi/180), m.cos(-_orientation[1]*m.pi/180)]]
        self.constants = MU*_current/(4*m.pi)
    #gets the field strength of a point around a straight wire
    def get(self, point):
        #applys translations and rotations relative to model origin
        x, y, z = np.subtract(point, self.location)
        x, y = rotate(x, y, self.rOrientation[0])
        x, z = rotate(x, z, self.rOrientation[1])

        #orients plane so that we are on the ax plane
        a = m.sqrt(y**2+z**2)

        #if the point P lies on the wire field strength is always zero therfore the function returns zero to avoid a divide by zero error
        if(a == 0): return([0] * 3)

        #calculates the bounds of the integral
        thetaMin = m.atan2(x-self.length*0.5, a)
        thetaMax = m.atan2(x+self.length*0.5, a)

        #finds the field strength perpendicular to the ax plane
        fieldStrength = self.constants*m.sin(thetaMax)-m.sin(thetaMin)/a
        
        #finds the angle to rotate the az plane vector
        phi = m.atan2(z, y)
        
        #rotates vector back into our models cartisien space
        u = 0
        v = -fieldStrength*m.sin(phi)
        w = fieldStrength*m.cos(phi)

        #rotates vector back into world space
        u, v = rotate(u, v, self.fOrientation[0])
        u, w = rotate(u, w, self.fOrientation[1])
        
        #returns vector
        return [u, v, w]

#rotates a point [x, y] on its respective plane by an angle theta  
def rotate(x, y, theta):
    u = x*theta[1]-y*theta[0]
    v = x*theta[0]+y*theta[1]
    return [u, v]