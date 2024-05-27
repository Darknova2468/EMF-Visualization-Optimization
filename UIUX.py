#libraries
import Plots as p
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import time

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

        #creates a grid for vector field graphs
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        #creates the frame work for the vector field graphs
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        #populates the grids with vector field graphs
        self.update_plot("XY", 0, 0)
        self.update_plot("YZ", 0, 1)
        self.update_plot("XZ", 1, 0)
        self.create_placeholder(1, 1)

        self.window.bind("<Configure>", self.on_resize)

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