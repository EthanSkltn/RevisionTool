import time
from tkinter import *
import os, glob
import customtkinter
from functools import partial
from collections import deque
import math
import pyodbc
#the imports of tkinter libraries.
root = Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

root.geometry("1100x700")
root.title("Application")
 
os.chdir("./File folder/")

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

class AddQuestions:
    def __init__(self):
        self.subjects_array = ["Mathematics","English","Science","Spanish","Psychology","Computer Science"]
        self.difficulty_array = ["Easy","Moderate","Intermediate","Medium","Difficult","Challenge","Expert","Impossible"]
        clear_window()
        self.setup_ui()
        self.add_items()
        
    def setup_ui(self):
        self.q_label = customtkinter.CTkLabel(root,text="Input question")
        self.q_label.pack()

        self.question = customtkinter.CTkEntry(root)
        self.question.pack()

        self.a_label = customtkinter.CTkLabel(root,text="Input answer")
        self.a_label.pack()

        self.answer = customtkinter.CTkEntry(root)
        self.answer.pack()

        self.ed_type_label = customtkinter.CTkLabel(root,text="Input type of education (e.g. GCSE , A-level)")
        self.ed_type_label.pack()

        self.ed_level = customtkinter.CTkEntry(root)
        self.ed_level.pack()

        self.sub_label = customtkinter.CTkLabel(root,text="Input subject")
        self.sub_label.pack()

        self.subject = customtkinter.CTkComboBox(root)
        self.subject.pack()

        self.dif_label = customtkinter.CTkLabel(root)
        self.dif_label.pack()

        self.difficulty = customtkinter.CTkComboBox(root)
        self.difficulty.pack()

        self.save = customtkinter.CTkButton(root,text="Save question",command=self.save_question)
        self.save.pack(pady=5)

    def add_items(self):
        self.subject.set("Select subject")
        self.subject.configure(values = self.subjects_array)
        
        self.difficulty.set("Select difficulty")
        self.difficulty.configure(values = self.difficulty_array)

    def save_question(self):
        self.information = cursor.execute("""SELECT *
                                          FROM Questions
                                          INNER JOIN Subjects ON Questions.subject_id = Subjects.subject_id
                                          INNER JOIN DifficultyLevels ON Questions.difficulty_id = DifficultyLevels.difficulty_id
                                          """).fetchall()
        in_question = self.question.get()
        in_answer = self.answer.get()
        in_subject = self.subject.get()
        in_education_level = self.ed_level.get()
        in_difficulty = self.difficulty.get()
        question_id = len(self.information)
        in_subject = self.subjects_array.index(in_subject)
        in_difficulty = self.difficulty_array.index(in_difficulty)
        print(in_subject,in_difficulty)
        cursor.execute("""INSERT INTO Questions (question_id,subject_id,difficulty_id,question,answer,education_type)
                       VALUES (?,?,?,?,?,?)""",question_id,in_subject,in_difficulty,in_question,in_answer,in_education_level)
        connection.commit()
        self.__init__()

class ExamQuestions:
    def __init__(self,user_id, username):
        self.user_id = user_id
        self.username = username
        self.subjects_array = ["Mathematics","Spanish"]
        self.criteria_array = []
        self.given_answer_array = []
        self.answer_format = ""
        self.given_answer = ""
        self.score = int

        clear_window()
        self.start_screen()
        self.add_items()

        #methods initalised after so the variables can be defined

    def start_screen(self):
        self.selection_frame = customtkinter.CTkFrame(root,width=1000,height=450)
        self.selection_frame.pack()
 
        self.sub_label = customtkinter.CTkLabel(self.selection_frame,text="Input subject")
        self.sub_label.pack()

        self.subject = customtkinter.CTkComboBox(self.selection_frame)
        self.subject.pack()

        self.select_button = customtkinter.CTkButton(self.selection_frame,text="Practice this!",command=self.display_question)
        self.select_button.pack()

        self.question_area = customtkinter.CTkFrame(root, width=1000, height=450)

        self.question = customtkinter.CTkLabel(self.question_area,font=("Helvetica", 40))
        self.question.pack()
 
        self.answer_area = customtkinter.CTkFrame(root,width=1100)

        self.answer_advice = customtkinter.CTkLabel(self.answer_area,text="Do not include the format your answer should be in e.g. X =. The format should be provided already.")
        self.answer_advice.place(x=2,y=2)

        self.format = customtkinter.CTkLabel(self.answer_area)
        self.format.place(x=2,y=40)

        self.answer_input = customtkinter.CTkEntry(self.answer_area, font=("Helvetica", 20),width=1000)
        self.answer_input.place(x=70,y=40)
 
        self.enter_button = customtkinter.CTkButton(self.answer_area,width=70, height=70, command = self.check_question)
        self.enter_button.place(x=1000,y=50)

        self.results_frame = customtkinter.CTkFrame(root)

        self.question_display = customtkinter.CTkLabel(self.results_frame)
        self.question_display.pack()

        self.answer_display = customtkinter.CTkLabel(self.results_frame)
        self.answer_display.pack(pady=0)
    
        self.given_display = customtkinter.CTkLabel(self.results_frame)
        self.given_display.pack(pady=30)

        self.correct_indicator = customtkinter.CTkLabel(self.results_frame)
        self.correct_indicator.pack(pady=15)

        self.next_question_button = customtkinter.CTkButton(self.results_frame,text="Next question",command=self.display_question)
        self.next_question_button.pack()

    def add_items(self):
        self.subject.set("Select subject")
        self.subject.configure(values = self.subjects_array)

    def check_question(self):
        current_word = ""
        self.criteria_array = []
        self.given_answer_array = []
        for characters in self.current_answer:
            print(characters)
            if characters == " ":
                if current_word == "=":
                    self.answer_format = self.criteria_array[len(self.criteria_array)-1] + " ="
                else:
                    self.criteria_array.append(current_word)
                current_word = ""
            else:
                if characters != "\n":
                    current_word = current_word + characters

        if current_word != "":
            if " " not in current_word:
                if "\n" not in current_word:
                    self.criteria_array.append(current_word)
        current_word = ""
        
        self.given_answer = self.answer_input.get()
        for characters in self.given_answer:
            print(characters)
            if characters == " ":
                part_end = True
                self.given_answer_array.append(current_word)
                current_word = ""
            else:
                current_word = current_word + str(characters)
        if current_word != "":
            if " " not in current_word:
                self.given_answer_array.append(current_word)
        self.score = 0
        print(self.given_answer_array,self.criteria_array)
        for i in range(len(self.given_answer_array)):
            for j in range(len(self.criteria_array)):
                if self.given_answer_array[i] == self.criteria_array[j]:
                    self.score = self.score + 1
        try:
            self.percent = 100*(len(self.criteria_array)/self.score)
        except:
            self.percent = 0
        self.display_results()
        print(self.percent)

    def display_results(self):
        self.question_area.pack_forget()
        self.answer_area.place_forget()
        self.question_display.configure(text="This is the question:" + self.current_question)
        self.answer_display.configure(text="This is the answer:"+self.current_answer)
        self.given_display.configure(text="This is your answer:"+ self.given_answer)
        if self.percent > 70.0:
            self.correct_indicator.configure(text="Correct answer!")
        else:
            self.correct_indicator.configure(text="You got this question wrong!")
        self.results_frame.pack()
        self.difficulty_calculator()
        self.update_stats()

    def get_user_stats(self):
        self.user_stats = cursor.execute("""SELECT user_difficulty, questions_answered
                                         FROM Accounts
                                         WHERE account_id = ?""",self.user_id).fetchone()
        print(self.user_stats)
        self.real_difficulty = self.user_stats[0]
        self.difficulty = round(self.real_difficulty,0)
        self.questions_answered = self.user_stats[1]

    def update_stats(self):
        self.questions_answered = self.questions_answered + 1
        cursor.execute("""UPDATE Accounts
                       SET user_difficulty = ?, questions_answered = ?
                       WHERE account_id = ?""",self.new_difficulty,self.questions_answered,self.user_id)
        cursor.commit()

    def choose_question(self,subject):
        self.whole_question = cursor.execute("""SELECT question, answer, question_id, answer_format
                                          FROM Questions
                                          INNER JOIN Subjects ON Questions.subject_id = Subjects.subject_id
                                          WHERE difficulty_id = ? AND subject_name = ?
                                          """,self.difficulty,subject).fetchone()
        print(self.whole_question)
        self.current_question = self.whole_question[0]
        self.current_answer=self.whole_question[1]
        self.current_id = self.whole_question[2]
        self.question_format = self.whole_question[3]

    def display_question(self):
        self.results_frame.pack_forget()
        self.get_user_stats()
        self.answer_input.delete(0,END)
        in_subject = self.subject.get()
        self.selection_frame.pack_forget()
        self.choose_question(in_subject)
        self.question_area.pack()
        self.question.pack(padx=5,pady=10)
        self.question.configure(text=self.current_question)
        if self.question_format == None:
            self.format.configure(text="")
        else:
            self.format.configure(text=self.question_format)
        self.answer_area.place(x=0,y=300)


    def difficulty_calculator(self):
        increase = 2.0
        if self.percent < 70:
            increase = -(increase)
            if len(self.criteria_array) < 3:
                try:
                    increase = increase*(1-(self.percent/100))
                except:
                    increase = increase*0.8
        if self.questions_answered == 0:
            increase = increase/0.9
        else:
            increase = increase/((math.log(self.questions_answered))+0.7)
        self.new_difficulty = self.real_difficulty + increase
        if self.new_difficulty > 7:
            self.new_difficulty = 7
        if self.new_difficulty < 0:
            self.new_difficulty = 0
        #calculating the change difficulty from 4 variables to allow the array to adapt to the cercumstances. More questions the less fluctuation in the difficulty. Less words to get correct the less of a penalty to getting it wrong. Percentage and current difficulty are the variables which indicate the final outcome.

        
login_system1 = ExamQuestions(0,"Admin")

root.mainloop()

