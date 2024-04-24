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


connection = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=ETHANS-LAPTOP;'
    'Database=NEA project;'
    'Trusted_Connection=yes;'
    )

cursor = connection.cursor() 

def clear_window():
        frames = [root]
        for frame in frames:
            for widget in frame.winfo_children():
                widget.destroy()

root = Tk()
root.configure(background="light grey")

delete_image_pil = Image.open("Delete image.png")

delete_image_pil_resized = delete_image_pil.resize((20, 20), Image.LANCZOS)

# Create a PhotoImage object
delete_image = ImageTk.PhotoImage(delete_image_pil_resized)


class Flashcard_System:
    def __init__ (self,root, user_id, username):
        self.username = username
        self.user_id = user_id
        
        self.whole_card = ""
        self.cards_array = []
        self.accuracy_score_array = []
        self.times_recalled_array = []
        self.next_recall_array = []
        self.flashid_array = []

        self.i=0

        self.load_existing_cards()
        clear_window()
        self.setup_ui()
        
        self.count = self.my_text1.bind("<Key>", self.count_flashcards)
        
    
    def setup_ui(self):
        self.create_frame = customtkinter.CTkFrame(root, width=1000, height=1080)
        self.create_frame.place(x=0, y=0)

        self.cards_frame = customtkinter.CTkFrame(root, width=500, height=500)
        self.cards_frame.place(x=1020, y=0)

        self.label_create = customtkinter.CTkLabel(self.create_frame, text="Create flashcards:", font=("Helvetica", 40), text_color="Navy")
        self.label_create.place(x=40, y=30)

        self.my_text1 = customtkinter.CTkTextbox(self.create_frame, width=900, height=500,font=("Helvetica", 40))
        self.my_text1.place(x=30, y=100)

        self.confirm_card = customtkinter.CTkButton(self.create_frame, text="Confirm cards",command=self.create_flashcards)
        self.confirm_card.place(x=700, y=30)

        self.flashcards_canvas = customtkinter.CTkCanvas(self.cards_frame, width=495,height=780)
        self.flashcards_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.flashcard_scrollbar = customtkinter.CTkScrollbar(self.cards_frame, command=self.flashcards_canvas.yview)
        self.flashcard_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.flashcard_canvas_inner = customtkinter.CTkFrame(self.flashcards_canvas,width=500,height=900)
        self.flashcards_canvas.create_window((0, 0), window=self.flashcard_canvas_inner, anchor=NW)

        self.edit_label = customtkinter.CTkLabel(self.flashcard_canvas_inner,text="Click on flashcard to edit:", font=("Helvetica", 40), text_color="Navy")
        self.edit_label.pack(padx=15,pady=10)

        for cards in self.cards_array:
            flashcard = self.cards_array[self.i]
            flashcard = flashcard.replace("##", " ➝ ")
            end = False
            times_repeated = 0
            i=0
            word_start=0
            while end != True:
                i = i + 1
                try:
                    if flashcard[i] == " ":
                        word_start = i
                    
                    if i == 50:
                        i = i + times_repeated*50
                        flashcard = flashcard[:word_start] + "\n" + flashcard[word_start:]
                        times_repeated = times_repeated + 1
                except:
                    end = True
            if cards != "":
                frame = customtkinter.CTkFrame(self.flashcard_canvas_inner, height=150,width=400)
                frame.pack(pady=5, padx=0)
                
                label_card = customtkinter.CTkLabel(frame,text=flashcard, font=("Helvetica", 15))
                label_card.place(x=5,y=5)
                frame.bind("<Button-1>", partial(self.on_frame_click, self.i))
                delete_card = customtkinter.CTkButton(frame,fg_color="red",width=40,height=40,image=delete_image,text="",command=partial(self.remove_card,self.flashid_array[self.i]))
                delete_card.place(x=20,y=100)

            self.i = self.i + 1
            

        self.flashcard_canvas_inner.update_idletasks()
        self.flashcards_canvas.configure(scrollregion=self.flashcards_canvas.bbox("all"))
        self.flashcards_canvas.update_idletasks()
        self.flashcards_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.flashcards_canvas.configure(yscrollcommand=self.flashcard_scrollbar.set)

        self.front_label = customtkinter.CTkLabel(self.create_frame, text="Edit front of card:",font=("Helvetica", 25))
        self.front_entry = customtkinter.CTkEntry(self.create_frame,width=400,height=40,font=("Helvetica", 20))
        self.arrow_label = customtkinter.CTkLabel(self.create_frame,text="➝",font=("Helvetica", 40))
        self.back_label = customtkinter.CTkLabel(self.create_frame, text="Edit back of card:",font=("Helvetica", 25))
        self.back_entry = customtkinter.CTkEntry(self.create_frame,width=400, height=40,font=("Helvetica", 20))

        self.confirm_edit = customtkinter.CTkButton(self.create_frame,text="Save changes->",command=self.save_changes)

    def reset_window(self):
        self.__init__(root,self.user_id,self.user_id)

    def remove_card(self, card):
        print(card)
        cursor.execute("""DELETE FROM Flashcards
                       WHERE flashcard_id = ?""",card)
        connection.commit()
        self.reset_window()

    def on_frame_click(self, number,event):
        #save current cards
        self.my_text1.place_forget()
        self.confirm_card.place_forget()
        self.front_label.place(x=150,y=200)
        self.front_entry.place(x=150,y=250)
        self.back_label.place(x=600,y=200)
        self.back_entry.place(x=600,y=250)
        self.confirm_edit.place(x=325,y=350)
        self.arrow_label.place(x=555,y=250)
        self.back_entry.delete(0,END)
        self.front_entry.delete(0,END)
        card = self.cards_array[number]
        middle = card.index("##")
        front = card[0:middle]
        back = card[middle+2:len(card)]
        print(back,front)
        self.front_entry.insert(0,front)
        self.back_entry.insert(0,back)
        self.current_editting = self.flashid_array[number]

    def save_changes(self):
        print(self.current_editting)
        self.new_card = self.front_entry.get() + "##" + self.back_entry.get()
        cursor.execute("""UPDATE Flashcards
                       SET flashcard = ?
                       WHERE flashcard_id = ?""",self.new_card, self.current_editting)
        connection.commit()
        self.cards_frame.update_idletasks()
        self.__init__(root,self.user_id,"Ethan4312")

    def on_mousewheel(self,event):
        self.flashcards_canvas.yview_scroll(-1*(event.delta//120), "units")

    def load_existing_cards(self):
        self.information = cursor.execute("""SELECT flashcard, flashcard_id, next_recall,
                                            times_recalled, accuracy_score
                                            FROM Flashcards""").fetchall()
        print(len(self.information))
        for rows in range(len(self.information)):
            self.cards_array.append(self.information[rows][0])
        for rows in range(len(self.information)):
            self.flashid_array.append(self.information[rows][1])
        for rows in range(len(self.information)):
            self.accuracy_score_array.append(self.information[rows][4])
        for rows in range(len(self.information)):
            self.times_recalled_array.append(self.information[rows][3])
        for rows in range(len(self.information)):
            self.next_recall_array.append(self.information[rows][2])
        

    def create_flashcards(self):
        lines = 0
        for letter in self.my_text1.get(0.0,END):
            #if there is a new line the lines count goes up 1
            if letter == "\n":
                lines = lines + 1
            #if there is a "➝" it enters the card creation
            if letter == "➝":
                print("CARD GETTING!")
                front = self.front_card(lines)
                back = self.back_card(lines)
                found = False
                i = 0
                
                while found == False:
                    if i not in self.flashid_array:
                        found = True
                    else:
                        i = i + 1
                    print(i)
                cursor.execute("""INSERT INTO Flashcards (account_id,flashcard_id,flashcard,accuracy_score,times_recalled,next_recall)
                            VALUES(?,?,?,0,0,0)""",self.user_id,i,str(front)+"##"+str(back))
                connection.commit()
                self.flashid_array.append(i)
        self.my_text1.delete(0.0,END)
        self.__init__(root,self.user_id,"Ethan4312")
        


    def front_card(self,lines):
        #the list which will be returned to the primary function to input into the file
        card_front = ""
        #the list which will contain all characters in the textbox
        text_list = []
        #the second line counter to allow the function to identify the line which the card is on
        line_count = 0
        #the variable to go through each value in the text_list list
        i = 0
        #the value which is used to break the while loops
        character = ""
        #looping through every character in the textbox and appending it to text_list
        for letter in self.my_text1.get(0.0,END):
            text_list.append(letter)
        #this loop can be broken by reaching a flashcard indicator
        while character != "➝":
            #incrimenting i
            i=i+1
            #incrimenting line_count for each line
            if text_list[i-1] == "\n":
                line_count = line_count + 1
            #identifies if the loop is on the correct line
            if line_count == lines:
                lines = lines + 1
                #this loop can be broken by reaching a flashcard indicator
                while character != "➝":
                    i = i + 1
                    #identification of the characters and adding any character other than "\n" and "➝"
                    if text_list[i-2] == "\n":
                        character = "\n"
                    elif text_list[i-2] == "➝":
                        character = "➝"
                    elif text_list[i-2] == '"':
                        card_front.append("'")
                    else:
                        card_front = card_front + (text_list[i-2])
        #returns the list of characters in the front of the card
        return card_front

    def back_card(self,lines):
        #the list which will be returned to the primary function to input into the file
        card_back = ""
        #the list which will contain all characters in the textbox
        text_list = []
        #the variable to go through each value in the text_list list
        i = 0
        #the second line counter to allow the function to identify the line which the card is on
        line_count = 0
        #a boolien variable which breaks the loop when true
        end_state = False
        #looping through every character in the textbox and appending it to text_list
        for letters in self.my_text1.get(0.0,END):
            text_list.append(letters)
        #initial loop to identify the correct line
        while end_state != True:
            i = i + 1
            if text_list[i] == "\n":
                line_count = line_count + 1
            if line_count == lines:
                i=i+1
                #the following loop to identify the start of the back of the card
                while end_state != True:
                    i = i+1
                    if text_list[i] == "➝":
                        i = i+1
                        #the loop which inserts all the characters into the card_back list and breaks once it reaches a "\n" or new line
                        while end_state != True:
                            i = i + 1
                            if text_list[i] == "\n":
                                end_state = True
                            else:
                                card_back = card_back + text_list[i]
        #returns the list of characters in the front of the card
        return card_back       
    
    def count_flashcards(self, value):
        #this variable is the count of hashtags in the textbox
        hashtag = 0
        #to loop through all the letters in the text box
        for letters in self.my_text1.get(0.0,END):
            #the if statement identifies the 1st instance of the "#"
            if letters == "#":
                hashtag = hashtag + 1
                #the next if statement identifies the 2nd hashtage as 2 in a row will result in the hashtag counter to = 2
                if hashtag == 2:
                    print("Flashcard created")
                    #to make sure the statement doesn't continuously repeat the variable is reset to 0
                    hashtag = 0
                    #this part replaces the "##" with the identifier of the flashcard
                    text_inside = self.my_text1.get(0.0,END)
                    text_inside = text_inside.replace("##","➝")
                    self.my_text1.delete(0.0,END)
                    self.my_text1.insert(END,text_inside)
            #this else ensures that if there is not a repeat of the "#" after a 1st input that the hashtag value is reset
            else:
                hashtag=0

#for i in range(60):
 #   card = "Front of flashcard" + str(i) + "##Back of flashcard" + str(i)
  #  cursor.execute("""INSERT INTO Flashcards (account_id, flashcard, flashcard_id, next_recall,
   #                                      times_recalled, accuracy_score)
    #                                     VALUES(?,?,?,0,0,0)""",1,card,i)
    #connection.commit()

flashcard_area = Flashcard_System(root, 1, "Ethan4312")
root.mainloop()

