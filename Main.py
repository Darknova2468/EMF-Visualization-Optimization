#libraries
import matplotlib.pyplot as plt # type: ignore # type: ignores
import numpy as np # type: ignore
import math as m
import Fields as f


#initializes the "coil" an array of wire elements
myCoil = f.Coil()

#adds elements
myCoil.addElement(f.Wire(10, [0,-0.5, 0.0], [0,0,0],  1))
myCoil.addElement(f.Wire(10, [0,0.5, 0.0], [0,0,0], -1))

# Fixed x value for the yz-plane
x_fixed = 0

# Set the grid width and generate the grid points for the yz-plane
w = 2
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