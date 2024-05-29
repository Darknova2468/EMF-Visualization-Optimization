#libraries
import UIUX as u
import GPUFieldsExp as f

#initializes the "coil" an array of wire elements
myCoil = f.RectCoil(0.2, 0.1, 0.1, 0.025, 0.0125)

#runs Application
if __name__ == "__main__":
    myApplication = u.newApplication(myCoil, 50)