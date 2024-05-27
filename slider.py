import numpy as np
import math as m
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Magnetic permittivity of free space
MU = 4 * m.pi * 10 ** -7

# Define global variables for slider values
global_slider_values = {"XY": 0, "YZ": 0, "XZ": 0}

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
        ax.set_aspect('equal', 'box')

        return fig

def update_plot(plane, row, column):
    pos = [[-3, 3], [-3, 3]]
    offset = 0  # Use a fixed offset or other logic as needed
    fig = myPlot.getPlot(plane, pos, offset)
    for widget in plot_frames[row][column].winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_frames[row][column])
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    plt.close(fig)  # Close the figure to free up resources

def create_placeholder(row, column):
    placeholder = tk.Frame(plot_frames[row][column], bg="grey")
    placeholder.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def create_slider(row, column, plane):
    slider_frame = tk.Frame(control_frames[row][column])
    slider_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    slider = tk.Scale(slider_frame, from_=-3, to=3, orient="vertical", length=300, resolution=0.1, command=lambda val: update_global_variable(plane, float(val)))
    slider.pack(side=tk.LEFT, fill=tk.Y, expand=True)
    slider.set(0)

def update_global_variable(plane, value):
    global_slider_values[plane] = value
    print(f"Updated {plane} plane slider value: {value}")

def main():
    global plot_frames, control_frames, myPlot
    myCoil = Coil()
    myCoil.addElement(Wire(4, [0, -2, 0.0], [180, 0], 1))
    myCoil.addElement(Wire(4, [0, 2, 0.0], [0, 0], 1))
    myCoil.addElement(Wire(4, [2, 0, 0.0], [270, 0], 1))
    myCoil.addElement(Wire(4, [-2, 0, 0.0], [90, 0], 1))

    myPlot = Plot(myCoil)

    window = tk.Tk()
    window.title("Magnetic Field Plots")
    window.geometry("1280x720")
    window.minsize(1280, 720)
    window.maxsize(1280, 720)

    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    plot_frames = [[None for _ in range(2)] for _ in range(2)]
    control_frames = [[None for _ in range(2)] for _ in range(2)]

    for i in range(2):
        for j in range(2):
            plot_frames[i][j] = tk.Frame(frame)
            plot_frames[i][j].grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
            plot_frames[i][j].grid_propagate(False)
            plot_frames[i][j].config(width=560, height=315)
            
            control_frames[i][j] = tk.Frame(frame)
            control_frames[i][j].grid(row=i, column=j, padx=10, pady=10, sticky="e")

    update_plot("XY", 0, 0)
    update_plot("YZ", 0, 1)
    update_plot("XZ", 1, 0)
    create_placeholder(1, 1)

    create_slider(0, 0, "XY")
    create_slider(0, 1, "YZ")
    create_slider(1, 0, "XZ")

    window.mainloop()

if __name__ == "__main__":
    main()
