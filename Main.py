#libraries
import matplotlib.pyplot as plt # type: ignore # type: ignores
import numpy as np # type: ignore
import math as m
import Fields as f

#initializes the "coil" an array of wire elements
myCoil = f.Coil()

#adds elements for a square loop of wire
myCoil.addElement(f.Wire(4, [0,2, 0.0], [0,0], 1))
myCoil.addElement(f.Wire(4, [2,0, 0.0], [270,0], 1))
myCoil.addElement(f.Wire(4, [0,-2, 0.0], [180,0], 1))
myCoil.addElement(f.Wire(4, [-2,0, 0.0], [90,0], 1))

# Fixed x value for the yz-plane
z_fixed = 0.5

# Set the grid width and generate the grid points for the yz-plane
w = 3
Y, X = np.mgrid[-w:w:500j, -w:w:500j]

# Initialize arrays for J and K components of the vector field
J = np.zeros_like(X)
K = np.zeros_like(Y)

# Apply the vector field function to each point in the yz-plane
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        J[i, j], K[i, j], _ = myCoil.get([X[i, j], Y[i, j], z_fixed])

# Calculate the magnitude of the vector field
magnitude = np.sqrt(J**2 + K**2)

#plots Vector Field
plt.streamplot(X, Y, J, K, color=magnitude, linewidth=2, cmap='viridis')
plt.colorbar(label='Speed')
plt.title('XY Plane EMF Field')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()