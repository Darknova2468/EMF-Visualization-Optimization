#libraries
import numpy as np # type: ignore
import math as m

#magnetic permuability of free space
MU = 4*m.pi*10**-7

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
        self.orientation = _orientation
        self.current = _current
    #gets the field strength of a point around a straight wire
    def get(self, point):
        #applys translations and rotations relative to model origin
        x, y, z = np.subtract(point, self.location)
        x, y = rotate(x, y, -self.orientation[0]*m.pi/180)
        x, z = rotate(x, z, -self.orientation[1]*m.pi/180)

        #orients plane so that we are on the ax plane
        a = m.sqrt(y**2+z**2)

        #if the point P lies on the wire field strength is always zero therfore the function returns zero to avoid a divide by zero error
        if(a == 0): return([0] * 3)

        #calculates the bounds of the integral
        thetaMin = m.atan2(x-self.length*0.5, a)
        thetaMax = m.atan2(x+self.length*0.5, a)

        #finds the field strength perpendicular to the ax plane
        integral = m.sin(thetaMax)-m.sin(thetaMin)
        magnitude = MU*self.current*integral/(4*m.pi*a)
        
        #finds the angle to rotate the az plane vector
        phi = m.atan2(z, y)
        
        #rotates vector back into our models cartisien space
        u = 0
        v = -magnitude*m.sin(phi)
        w = magnitude*m.cos(phi)

        #rotates vector back into world space
        u, v = rotate(u, v, self.orientation[0]*m.pi/180)
        u, w = rotate(u, w, self.orientation[1]*m.pi/180)
        
        #returns vector
        return [u, v, w]

#rotates a point [x, y] on its respective plane by an angle theta  
def rotate(x, y, theta):
    u = x*m.cos(theta)-y*m.sin(theta)
    v = x*m.sin(theta)+y*m.cos(theta)
    return [u, v]