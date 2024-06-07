#libraries
import UIUX as u
import Fields as f

#initializes the "coil" an array of wire elements
myCoil = f.RectCoil(0.1, 0.1, 0.0251, 0.0251, 0.005)

#runs Application
if __name__ == "__main__":
    myApplication = u.newApplication(myCoil, 50)