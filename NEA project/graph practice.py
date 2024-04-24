import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GraphPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter App")
        self.create_widgets()

    def create_widgets(self):
        self.plot_button = ttk.Button(self.root, text="Plot Graph", command=self.plot_graph)
        self.plot_button.pack(pady=10)

    def plot_graph(self):
        # Generate sample data
        x = np.linspace(0, 100, 100)
        y = np.y=x+2, 4<x<9

        # Create a figure and axis
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y)

        # Create a canvas to display the plot
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphPlotterApp(root)
    root.mainloop()
