# Libraries
import GPUFieldsExp as p
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from multiprocessing import Process, Queue
import time
import logging

# Define global variables for slider values
global_slider_values = {"XY": 0, "YZ": 0, "XZ": 0}

def compute_plot(queue, plot, plane, pos, offset):
    logger = logging.getLogger()
    logger.debug("Starting compute_plot")
    fig = plot.getPlot(plane, pos, offset)
    logger.debug("Plot generated")
    queue.put((plane, fig, None))

class newApplication:
    # Initializes all constraints and starts the main loop of application
    def __init__(self, _coil, _resolution=0):
        # Creates a plot object from whatever coil is attempting to be visualized
        self.coil = _coil
        self.plot = p.plot(_coil, _resolution) if _resolution != 0 else p.plot(_coil)

        # Starts and labels window
        self.window = tk.Tk()
        self.window.title("Magnetic Field Plots")
        self.window.geometry("920x720")
        self.window.minsize(920, 720)
        self.window.maxsize(920, 720)

        # Creates a grid for vector field graphs
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Creates the framework for the vector field graphs
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

        # Populates the grids with vector field graphs
        self.update_plot()
        self.create_placeholder(1, 1)

        self.create_slider(0, 0, "XY")
        self.create_slider(0, 1, "YZ")
        self.create_slider(1, 0, "XZ")

        # Opens application
        self.window.mainloop()

    # Dynamically resizes window
    def on_resize(self, event):
        self.window.update_idletasks()

    # Creates a blank frame to fill empty grid spot
    def create_placeholder(self, row, column):
        placeholder = tk.Frame(self.frame, bg="grey")
        placeholder.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    # Handles the plot update by offloading the computation to a separate process
    def update_plot(self):
        startTime = time.time()
        x, y, z = self.coil.dim[0]*1.5, self.coil.dim[1]*1.5, self.coil.dim[2]*1.5
        a = max(x, y, z)
        pos = [[-a, a], [-a, a]]

        self.queue = Queue()
        self.processes = []

        # Define the processes for each plane
        for plane in ["XY", "YZ", "XZ"]:
            offset = 0.0125 if plane == "XY" else 0
            p = Process(target=compute_plot, args=(self.queue, self.plot, plane, pos, offset))
            self.processes.append(p)
            p.start()
        # Join the processes and get the results
        self.figures = {}
        print("joinining?")
        self.processes[0].join()
        print("joined0")
        self.processes[1].join()
        print("joined1")
        self.processes[2].join()
        print("joined2")
        plane, fig, error = self.queue.get()
        if error:
            print(f"Error in process for plane {plane}: {error}")
        else:
            self.figures[plane] = fig

        # Update the plots in the UI
        self.update_canvas("XY", 0, 0)
        self.update_canvas("YZ", 0, 1)
        self.update_canvas("XZ", 1, 0)

        print(f'{time.time() - startTime}s for all plots at resolution: {self.plot.resolution}')

    # Updates the canvas with the generated figure
    def update_canvas(self, plane, row, column):
        if plane in self.figures:
            fig = self.figures[plane]
            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    def create_slider(self, row, column, plane):
        slider_frame = tk.Frame(self.control_frames[row][column])
        slider_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        slider = tk.Scale(slider_frame, from_=-3, to=3, orient="vertical", length=300, resolution=0.1, command=lambda val: self.update_global_variable(plane, float(val)))
        slider.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        slider.set(0)

    def update_global_variable(self, plane, value):
        global_slider_values[plane] = value
        print(f"Updated {plane} plane slider value: {value}")