#libraries
import UIUX as u
import Fields as f
import Plots as p

#initializes the "coil" an array of wire elements
myCoil = f.RectCoil(0.2, 0.1, 0.1, 0.025, 0.002588)

#runs Application
print(myCoil.current)
print(f'{myCoil.get([0,0,0.0125])}T at N pole')
print(f'{myCoil.get([0,0,-0.0125])}T at S pole')
myApplication = u.newApplication(myCoil, 50)