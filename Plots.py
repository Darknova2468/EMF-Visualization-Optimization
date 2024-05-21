#libraries
import matplotlib.pyplot as plt # type: ignore # type: ignores
import numpy as np # type: ignore
import math as m
import Fields as f

class plot:
    def __init__(self, _coil, _resolution = 100):
        self.coil = _coil
        self.resolution = _resolution
    def getPlot(self, plane, pos, offset):
        # Set the grid width and generate the grid points for the plane (Generates Points)
        J, I = np.mgrid[pos[0][0]:pos[0][1]:complex(self.resolution), pos[1][0]:pos[1][1]:complex(self.resolution)]

        # Initialize arrays for U and V components of the vector field (Generates Vectors on those points)
        U = np.zeros_like(I)
        V = np.zeros_like(J)
        if(plane == "XY"):
            # Apply the vector field function to each point in the XY-plane (Plots those vectors on those points on the graph)
            for i in range(I.shape[0]):
                for j in range(I.shape[1]):
                    U[i, j], V[i, j], _ = self.coil.get([I[i, j], J[i, j], offset])
        elif(plane == "YZ"):
            # Apply the vector field function to each point in the YZ-plane (Plots those vectors on those points on the graph)
            for i in range(I.shape[0]):
                for j in range(I.shape[1]):
                    _, U[i, j], V[i, j] = self.coil.get([offset, I[i, j], J[i, j]])
        elif(plane == "XZ"):
            # Apply the vector field function to each point in the XZ-plane (Plots those vectors on those points on the graph)
            for i in range(I.shape[0]):
                for j in range(I.shape[1]):
                    U[i, j], _, V[i, j] = self.coil.get([I[i, j], offset, J[i, j]])
        else:
            #raises exception given an invalid input
            raise Exception('Sorry the required plane message needs to be either "XY", "YZ" or "XZ"')
        
        # Calculate the magnitude of the vector field
        magnitude = np.sqrt(U**2 + V**2)
        #plots Vector Field
        plt.figure()
        myPlot = plt.streamplot(I, J, U, V, color=magnitude, linewidth=2, cmap='viridis')
        plt.colorbar(label='FieldStrength (T)')
        plt.title(plane + ' Plane EMF Field')
        plt.xlabel(plane[0])
        plt.ylabel(plane[1])

        return myPlot
    def showPlot(self, plane, pos, offset): 
        self.getPlot(plane, pos, offset)
        plt.show()