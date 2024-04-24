import time
from tkinter import *
import tkinter as tk
import os, glob
import customtkinter
from customtkinter import CTkImage
from functools import partial
from collections import deque
import math
import pyodbc
from PIL import  Image, ImageTk , ImageFilter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

"""#6BBF90,#B0D9C1,#D9BCA3"""
colour_theme1 = "#6BBF90"
colour_theme2 = "#B0D9C1"
colour_theme3 = "#D9BCA3"

#the imports of tkinter libraries.
root = Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue") 

root.title("Application")
root.configure(background=colour_theme2)

def clear_window():
        frames = [root]
        for frame in frames:
            for widget in frame.winfo_children():
                widget.destroy()

class HomeScreen:
    def __init__(self):
          clear_window()
          self.setup_ui()

    def setup_ui(self):
        self.button_frame = customtkinter.CTkFrame(root,fg_color=colour_theme2,)
        self.button_frame.pack(pady=100)

        self.flashcard_practice = customtkinter.CTkButton(self.button_frame,text="Practice your flashcards",hover_color=colour_theme3,fg_color=colour_theme1,border_color=colour_theme2,border_width=3,width=600,height=300,command=self.run_flashcard_app)
        self.flashcard_practice.grid(column=1,row=0,padx=5,pady=5)

        self.flashcard_editting = customtkinter.CTkButton(self.button_frame,text="Create and edit your flashcards",hover_color=colour_theme3,fg_color=colour_theme1,border_color=colour_theme2,border_width=3,width=600,height=300,command=self.practice_flashcard_app)
        self.flashcard_editting.grid(column=0,row=1,padx=5,pady=5)

        self.files = customtkinter.CTkButton(self.button_frame,text="Create and add to your files",hover_color=colour_theme3,fg_color=colour_theme1,border_color=colour_theme2,border_width=3,width=600,height=300,command=self.run_files)
        self.files.grid(column=1,row=1,padx=5,pady=5)

        self.practice_exam_questions = customtkinter.CTkButton(self.button_frame,text="Practic subject specific exam questions",hover_color=colour_theme3,fg_color=colour_theme1,border_color=colour_theme2,border_width=3,width=600,height=300,command=self.practice_exam_app)
        self.practice_exam_questions.grid(column=0,row=0,padx=5,pady=5)

    def run_flashcard_app(self):
         pass
    def practice_flashcard_app(self):
         pass
    def run_files(self):
         pass
    def practice_exam_app(self):
         pass

new_home = HomeScreen()
root.mainloop()