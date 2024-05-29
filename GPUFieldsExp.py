# Libraries
import matplotlib.pyplot as plt  # type: ignore
import cupy as cp
import math as m
import logging

# Magnetic permeability of free space
MU = 4 * m.pi * 10**-7

class RectCoil:
    # Initializes the array of wire elements and if no elements are provided it initializes an empty array
    def __init__(self, _x, _y, _z, _w, _dia):
        self.elements = []
        self.current = 98000 * m.pow(_dia, 1.27)
        for z in range(int(-(_z/_dia-1)/2), int((_z/_dia-1)/2)):
            for n in range(int(_w/_dia-1)):
                self.elements.append(Wire(_x+(n+1)*_dia, [0, _y+(n+0.5)*_dia, -(z+0.5)*_dia], [0, 0]))
                self.elements.append(Wire(_y+(n+1)*_dia, [_x+(n+0.5)*_dia, 0, -(z+0.5)*_dia], [270, 0]))
                self.elements.append(Wire(_x+(n+1)*_dia, [0, -_y+(n+0.5)*_dia, -(z+0.5)*_dia], [180, 0]))
                self.elements.append(Wire(_y+(n+1)*_dia, [-_x+(n+0.5)*_dia, 0, -(z+0.5)*_dia], [90, 0]))
        self.dim = [_x+_w*2, _y+_w*2, _z]
        self.constants = MU * self.current / (4 * m.pi)
    # Gets the field strength of a point around the coil
    def get(self, plane):
        logger = logging.getLogger()
        logger.error(f"HEY IM RUNNING!")
        u, v, w = self.elements[0].get(plane)
        for i in range(1, len(self.elements)):
            u1, v1, w1 = self.elements[i].get(plane)
            u += u1
            v += v1
            w += w1
            
        u *= self.constants
        v *= self.constants
        w *= self.constants
        logger.error(f"Finished Lol")
        return u, v, w



class Wire:
    # Initializes all the parameters of the straight wire
    def __init__(self, _length, _location, _orientation):
        self.length = _length
        self.location = cp.array(_location)
        # Forward orientation or sin(theta), cos(theta)
        self.fOrientation = [[m.sin(_orientation[0] * m.pi / 180), m.cos(_orientation[0] * m.pi / 180)], 
                             [m.sin(_orientation[1] * m.pi / 180), m.cos(_orientation[1] * m.pi / 180)]]
        # Reverse orientation or sin(-theta), cos(-theta)
        self.rOrientation = [[m.sin(-_orientation[0] * m.pi / 180), m.cos(-_orientation[0] * m.pi / 180)], 
                             [m.sin(-_orientation[1] * m.pi / 180), m.cos(-_orientation[1] * m.pi / 180)]]

    # Gets the field strength of a point around a straight wire
    def get(self, plane):
        xyz = plane - self.location

        x1, y = self.rotate(xyz[:,:,0], xyz[:,:,1], self.rOrientation[0])
        x2, z = self.rotate(x1, xyz[:,:,2], self.rOrientation[1])

        a = cp.linalg.norm(cp.stack((y,z), axis=1), axis=1)

        endPoint1 = x2-(self.length*0.5)
        endPoint2 = x2+(self.length*0.5)

        thetaMin = cp.arctan2(endPoint1, a)
        thetaMax = cp.arctan2(endPoint2, a)

        integral = (cp.sin(thetaMax)-cp.sin(thetaMin))/a

        phi = cp.arctan2(z, y)

        x = cp.zeros_like(a)
        y = -integral*cp.sin(phi)
        z = integral*cp.cos(phi)

        u1, v = self.rotate(x, y, self.fOrientation[0])
        u2, w = self.rotate(u1, z, self.fOrientation[1])

        return u2, v, w
    #rotates a point [x, y] on its respective plane by an angle theta  
    def rotate(self, x, y, theta):
        u = x*theta[1]-y*theta[0]
        v = x*theta[0]+y*theta[1]
        return u, v
    
class plot:
    def __init__(self, _coil, _resolution=100):
        self.coil = _coil
        self.resolution = _resolution

    def getPlot(self, plane, pos, offset):
        # Set the grid width and generate the grid points for the plane (Generates Points)
        I_values = cp.linspace(pos[0][0], pos[0][1], self.resolution)
        J_values = cp.linspace(pos[1][0], pos[1][1], self.resolution)
        I, J = cp.meshgrid(I_values, J_values)
        K = cp.full_like(I, offset)

        if plane == "XY":
            # Apply the vector field function to each point in the XY-plane
            grid = cp.stack((I, J, K), axis=-1)
        elif plane == "YZ":
            # Apply the vector field function to each point in the YZ-plane
            grid = cp.stack((K, I, J), axis=-1)
        elif plane == "XZ":
            # Apply the vector field function to each point in the XZ-plane
            grid = cp.stack((I, K, J), axis=-1)
        
        X, Y, Z = self.coil.get(grid)

        if plane == "XY":
            U, V = X, Y
        elif plane == "YZ":
            U, V = Y, Z
        elif plane == "XZ":
            U, V = X, Z

        # Calculate the magnitude of the vector field
        magnitude = cp.sqrt(U**2 + V**2)

        # Convert CuPy arrays to NumPy arrays for plotting
        U_np = cp.asnumpy(U)
        V_np = cp.asnumpy(V)
        I_np = cp.asnumpy(I_values)
        J_np = cp.asnumpy(J_values)
        magnitude_np = cp.asnumpy(magnitude)

        # Plots Vector Field
        fig, ax = plt.subplots(figsize=(3, 3))
        strm = ax.streamplot(I_np, J_np, U_np, V_np, color=magnitude_np, linewidth=1, cmap='viridis')
        fig.colorbar(strm.lines, label='Field Strength (T)')
        ax.set_title(f'{plane} Plane EMF Field')
        ax.set_xlabel(plane[0])
        ax.set_ylabel(plane[1])

        return fig