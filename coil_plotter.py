import numpy as np
import math as m
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Magnetic permittivity of free space
MU = 4 * m.pi * 10 ** -7

class Coil:
    def __init__(self, _elements=[]):
        self.elements = _elements

    def addElement(self, element):
        self.elements.append(element)
        return

    def get(self, point):
        fieldStrength = [0, 0, 0]
        for element in self.elements:
            fieldStrength = np.add(fieldStrength, element.get(point))
        return fieldStrength

class Wire:
    def __init__(self, _length, _location, _orientation, _current):
        self.length = _length
        self.location = _location
        self.orientation = _orientation
        self.current = _current

    def get(self, point):
        x, y, z = np.subtract(point, self.location)
        x, y = rotate(x, y, -self.orientation[0] * m.pi / 180)
        x, z = rotate(x, z, -self.orientation[1] * m.pi / 180)
        a = m.sqrt(y ** 2 + z ** 2)

        if a == 0:
            return [0] * 3

        thetaMin = m.atan2(x - self.length * 0.5, a)
        thetaMax = m.atan2(x + self.length * 0.5, a)
        integral = m.sin(thetaMax) - m.sin(thetaMin)
        magnitude = MU * self.current * integral / (4 * m.pi * a)
        phi = m.atan2(z, y)
        
        u = 0
        v = -magnitude * m.sin(phi)
        w = magnitude * m.cos(phi)
        
        u, v = rotate(u, v, self.orientation[0] * m.pi / 180)
        u, w = rotate(u, w, self.orientation[1] * m.pi / 180)
        return [u, v, w]

def rotate(x, y, theta):
    u = x * m.cos(theta) - y * m.sin(theta)
    v = x * m.sin(theta) + y * m.cos(theta)
    return [u, v]

class Plot:
    def __init__(self, _coil, _resolution=100):
        self.coil = _coil
        self.resolution = _resolution

    def getPlot(self, plane, pos, offset):
        J, I = np.mgrid[pos[0][0]:pos[0][1]:complex(self.resolution), pos[1][0]:pos[1][1]:complex(self.resolution)]
        U = np.zeros_like(I)
        V = np.zeros_like(J)

        if plane == "XY":
            for i in range(I.shape[0]):
                for j in range(I.shape[1]):
                    U[i, j], V[i, j], _ = self.coil.get([I[i, j], J[i, j], offset])
        elif plane == "YZ":
            for i in range(I.shape[0]):
                for j in range(I.shape[1]):
                    _, U[i, j], V[i, j] = self.coil.get([offset, I[i, j], J[i, j]])
        elif plane == "XZ":
            for i in range(I.shape[0]):
                for j in range(I.shape[1]):
                    U[i, j], _, V[i, j] = self.coil.get([I[i, j], offset, J[i, j]])
        else:
            raise Exception('Invalid plane. Must be "XY", "YZ", or "XZ"')

        magnitude = np.sqrt(U ** 2 + V ** 2)
        fig, ax = plt.subplots(figsize=(3, 3))
        strm = ax.streamplot(I, J, U, V, color=magnitude, linewidth=1, cmap='viridis')
        fig.colorbar(strm.lines, label='Field Strength (T)')
        ax.set_title(f'{plane} Plane EMF Field')
        ax.set_xlabel(plane[0])
        ax.set_ylabel(plane[1])

        return fig

def update_plot(plane, row, column):
    pos = [[-3, 3], [-3, 3]]
    offset = 0
    fig = myPlot.getPlot(plane, pos, offset)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

def create_placeholder(row, column):
    placeholder = tk.Frame(frame, bg="grey")
    placeholder.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

def on_resize(event):
    window.update_idletasks()

myCoil = Coil()
myCoil.addElement(Wire(4, [0, -2, 0.0], [180, 0], 1))
myCoil.addElement(Wire(4, [0, 2, 0.0], [0, 0], 1))
myCoil.addElement(Wire(4, [2, 0, 0.0], [270, 0], 1))
myCoil.addElement(Wire(4, [-2, 0, 0.0], [90, 0], 1))

myPlot = Plot(myCoil)

window = tk.Tk()
window.title("Magnetic Field Plots")

frame = tk.Frame(window)
frame.grid(row=0, column=0, sticky="nsew")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

update_plot("XY", 0, 0)
update_plot("YZ", 0, 1)
update_plot("XZ", 1, 0)
create_placeholder(1, 1)

window.bind("<Configure>", on_resize)

window.mainloop()
