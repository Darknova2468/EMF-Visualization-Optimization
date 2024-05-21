#libraries
import matplotlib.pyplot as plt # type: ignore # type: ignores
import numpy as np # type: ignore
import math as m
import Fields as f
import Plots as p


#initializes the "coil" an array of wire elements
myCoil = f.Coil()

#adds elements
myCoil.addElement(f.Wire(10, [0,-0.5, 0.0], [0,0,0],  1))
myCoil.addElement(f.Wire(10, [0,0.5, 0.0], [0,0,0], -1))

myPlot = p.plot(myCoil, 100)

myPlot.showPlot("YZ", [[-3, 3],[-3,3]], 0)