#libraries
import UIUX as u
import Fields as f
import Plots as p

#initializes the "coil" an array of wire elements
myCoil = f.Coil()

#adds elements for a square loop of wire
myCoil.addElement(f.Wire(4, [0,2, 0.0], [0,0], 1))
myCoil.addElement(f.Wire(4, [2,0, 0.0], [270,0], 1))
myCoil.addElement(f.Wire(4, [0,-2, 0.0], [180,0], 1))
myCoil.addElement(f.Wire(4, [-2,0, 0.0], [90,0], 1))

#runs Application
myApplication = u.newApplication(myCoil, 100)