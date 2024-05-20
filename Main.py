#libraries
import matplotlib.pyplot as plt # type: ignore # type: ignores
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
        #applys translations relative to world origin
        x = point[0]+self.location[0]
        y = point[1]+self.location[1]
        z = point[2]+self.location[2]

        #initializes fieldstrength array
        fieldStrength = [0] * 3

        #orients plane so that we are on the ax plane
        a = m.sqrt(y**2+z**2)

        #if the point P lies on the wire field strength is always zero therfore the function returns zero to avoid a divide by zero error
        if(a == 0): return(fieldStrength)

        #calculates the bounds of the integral
        thetaMin = m.atan2(x-self.length*0.5, a)
        thetaMax = m.atan2(x+self.length*0.5, a)

        #finds the field strength perpendicular to the ax plane
        integral = m.sin(thetaMax)-m.sin(thetaMin)
        magnitude = MU*self.current*integral/(4*m.pi*a)
        
        #finds the angle to rotate the az plane vector
        phi = m.atan2(y, z)
        
        #rotates vector back into our cartisien space
        fieldStrength[1] = magnitude*m.sin(phi)
        fieldStrength[2] = magnitude*m.cos(phi)

        #returns vector
        return fieldStrength

#initializes the "coil" an array of wire elements
myCoil = Coil()

#adds elements
myCoil.addElement(Wire(10, [0,0,0], [0,0,0], 1))

# Fixed x value for the yz-plane
x_fixed = 0

# Set the grid width and generate the grid points for the yz-plane
w = 1
Z, Y = np.mgrid[-w:w:500j, -w:w:500j]

# Initialize arrays for J and K components of the vector field
J = np.zeros_like(Y)
K = np.zeros_like(Z)

# Apply the vector field function to each point in the yz-plane
for i in range(Y.shape[0]):
    for j in range(Y.shape[1]):
        _, J[i, j], K[i, j] = myCoil.get([x_fixed, Y[i, j], Z[i, j]])

# Calculate the magnitude of the vector field
magnitude = np.sqrt(J**2 + K**2)

#plots Vector Field
plt.streamplot(Y, Z, J, K, color=magnitude, linewidth=2, cmap='viridis')
plt.colorbar(label='Speed')
plt.title('YZ Plane EMF Field')
plt.xlabel('Y')
plt.ylabel('Z')
plt.show()