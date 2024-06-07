#libraries
import GPUFieldsExp as p
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
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

        x = self.coil.dim[0]*1.5
        y = self.coil.dim[1]*1.5
        z = self.coil.dim[2]*1.5
        a = max(x, y, z)
        self.pos = [[-a, a],[-a, a],[-a, a]]
        self.plot.getBField(self.pos)

        #starts and labels window
        self.window = tk.Tk()
        self.window.title("Magnetic Field Plots")
        self.window.geometry("1920x1080")
        self.window.minsize(1920, 1080)
        self.window.maxsize(1920, 1080)

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
        offset = global_slider_values[plane]
        fig = self.plot.getPlane(plane, self.pos, offset)

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=row, column=column, padx=100, pady=10, sticky="W")
        canvas_widget.configure(width=500, height=400)

    def create_slider(self, row, column, plane):
        self.slider_frame = tk.Frame(self.control_frames[row][column], padx=100)
        self.slider_frame = tk.Frame(self.control_frames[row][column], padx=100)
        self.slider_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.slider = tk.Scale(self.slider_frame, from_=self.pos[0][0], to=self.pos[0][1], orient="vertical", length=300, resolution= (self.pos[2][1] - self.pos[2][0]) / (self.plot.resolution - 1), command=lambda val: self.update_global_variable(plane, float(val)))
        self.slider.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.slider.set(0)

    def update_global_variable(self, plane, value):
        global_slider_values[plane] = value
        if(plane == "XY"):
            self.update_plot(plane, 0, 0)
        elif(plane == "YZ"):
            self.update_plot(plane, 0, 1)
        elif(plane == "XZ"):
            self.update_plot(plane, 1, 0)