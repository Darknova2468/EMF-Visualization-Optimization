#libraries
import GPUFieldsExp as p
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from multiprocess import process as mp
import time

# Define global variables for slider values
global_slider_values = {"XY": 0, "YZ": 0, "XZ": 0}

class newApplication:
    #initializes all constraints and starts the main loop of application
    def __init__(self, _coil, _resolution = 0):
        #creates a plot object from whatever coil is attempting to be visualized
        self.coil = _coil
        if _resolution == 0:
            self.plot = p.plot(_coil)
        else:
            self.plot = p.plot(_coil, _resolution)

        #starts and labels window
        self.window = tk.Tk()
        self.window.title("Magnetic Field Plots")
        self.window.geometry("920x720")
        self.window.minsize(920, 720)
        self.window.maxsize(920, 720)

        #creates a grid for vector field graphs
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.BOTH, expand=True)

        #creates the frame work for the vector field graphs
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.plot_frames = [[None for _ in range(2)] for _ in range(2)]
        self.control_frames = [[None for _ in range(2)] for _ in range(2)]

        for i in range(2):
            for j in range(2):
                self.plot_frames[i][j] = tk.Frame(self.frame)
                self.plot_frames[i][j].grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                self.plot_frames[i][j].grid_propagate(False)
                self.plot_frames[i][j].config(width=560, height=315)
                
                self.control_frames[i][j] = tk.Frame(self.frame)
                self.control_frames[i][j].grid(row=i, column=j, padx=10, pady=10, sticky="e")

        #populates the grids with vector field graphs
        self.update_plot("XY", 0, 0)
        self.update_plot("YZ", 0, 1)
        self.update_plot("XZ", 1, 0)
        self.create_placeholder(1, 1)

        self.create_slider(0, 0, "XY")
        self.create_slider(0, 1, "YZ")
        self.create_slider(1, 0, "XZ")

        #opens application
        self.window.mainloop()

    #dynamically resizes window
    def on_resize(self, event):
        self.window.update_idletasks()

    #creates a blank frame to fill empty grid spot
    def create_placeholder(self, row, column):
        placeholder = tk.Frame(self.frame, bg="grey")
        placeholder.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    #fills the input frame with a vector field plot from Plots.py
    def update_plot(self, plane, row, column):
        startTime = time.time()
        x = self.coil.dim[0]*1.5
        y = self.coil.dim[1]*1.5
        z = self.coil.dim[2]*1.5
        a = max(x, y, z)
        pos = [[-a, a],[-a, a]]
        offset = 0
        if(plane == "XY"): offset = 0.0125
        fig = self.plot.getPlot(plane, pos, offset)
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        print(f'{startTime - time.time()}s for {plane} at resolution:{self.plot.resolution}')

    def create_slider(self, row, column, plane):
        self.slider_frame = tk.Frame(self.control_frames[row][column])
        self.slider_frame = tk.Frame(self.control_frames[row][column])
        self.slider_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.slider = tk.Scale(self.slider_frame, from_=-3, to=3, orient="vertical", length=300, resolution=0.1, command=lambda val: self.update_global_variable(plane, float(val)))
        self.slider.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.slider.set(0)

    def update_global_variable(self, plane, value):
        global_slider_values[plane] = value
        print(f"Updated {plane} plane slider value: {value}")