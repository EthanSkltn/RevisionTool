import math
import tkinter as tk
import customtkinter
from functools import partial
from collections import deque
import os
import re


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")


class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.already_done = deque()
        #Seperate attributes
        
        self.all_cards = ""
        self.cards_array = []
        self.is_quote = False
        self.front_card = ""
        self.whole_card = ""
        self.front_card_text = ""
        self.back_card_text = ""
        #Whole flashcard attributes

        self.stats_array = []
        self.current_card_stats = ""
        self.old_stats = ""
        #Flashcard statistic attributes

        self.current_card = 0
        self.is_hashtag = False
        self.hashtag_count = 0
        #Attributes used throughout the methods
        
        self.difficulty = ""
        self.accuracy_score_pattern = str or int
        self.times_recalled_pattern = str or int
        self.next_recall = str or int
        self.improvements_required = bool
        #Attributes identified and updating the cards statistics
        
        self.load_flashcard_stats()
        self.load_flashcards()
        self.setup_ui()
        #methods initalised after so the variables can be defined

    def setup_ui(self):
        self.question_frame = customtkinter.CTkFrame(root,width=1100,height=600)
        self.question_frame.place(x=0,y=0)

        self.front_card_question = customtkinter.CTkLabel(self.question_frame,text=self.get_front()+" ➝ ?",font=("Helvetica", 33))
        self.front_card_question.place(x=50,y=50)

        self.show_button = customtkinter.CTkButton(self.question_frame, text="Show answer",width=1000,height=60,command=self.show_back)
        self.show_button.place(x=50,y=500)

        self.answer_frame = customtkinter.CTkFrame(root,height=600,width=1100)

        self.back_card_answer = customtkinter.CTkLabel(self.answer_frame,text=self.get_front() + " ➝ " +self.get_back(),font=("Helvetica", 33))
        self.back_card_answer.place(x=50,y=50)

        self.skip_button = customtkinter.CTkButton(self.answer_frame,text="Skip", command=partial(self.card_running_system,"Skip"))
        self.skip_button.place(x=150,y=500)

        self.easy_button = customtkinter.CTkButton(self.answer_frame,text="Easy", command=partial(self.card_running_system,"Easy"))
        self.easy_button.place(x=400,y=500)

        self.managed_button = customtkinter.CTkButton(self.answer_frame,text="Managed", command=partial(self.card_running_system,"Managed"))
        self.managed_button.place(x=650,y=500)

        self.challenging_button = customtkinter.CTkButton(self.answer_frame,text="Challenge", command=partial(self.card_running_system,"Challenge"))
        self.challenging_button.place(x=900,y=500)

        self.improvements_frame = customtkinter.CTkFrame(root,width=1100,height=600)

        self.improvements_text = customtkinter.CTkLabel(self.improvements_frame,text="Maybe you should cosider altering your flashcard to help it stick in your memory, as you seam to be having trouble recalling this card.")
        self.improvements_text.place(x=50,y=30)

        self.edit_card_button = customtkinter.CTkButton(self.improvements_frame, text="Edit flashcard")
        self.edit_card_button.place(x=50,y=400)

        self.pass_improvements = customtkinter.CTkButton(self.improvements_frame,text="Maybe later",command=self.show_front,width=1000,height=60)
        self.pass_improvements.place(x=50,y=500)

    def load_flashcards(self):
        # Load flashcards from file and initialize data structures
        file = open("Flashcard file.txt","r")
        self.whole_card = file.read()
        file.close()
        self.is_quote = False
        for characters in self.whole_card:
            if self.is_quote == True and characters != '"':
                self.front_card = self.front_card + characters
            if characters == '"':
                self.is_quote = not self.is_quote
                if self.is_quote == False:
                    self.cards_array.append(self.front_card)
                    self.front_card = ""

    def load_flashcard_stats(self):
        file = open("Flashcard file.txt","r")
        self.whole_card = file.read()
        file.close()
        self.current_card_stats = ""
        self.is_quote = True
        for characters in self.whole_card:
            if self.is_quote == True and characters != '\n' and characters != '"':
                self.current_card_stats = self.current_card_stats + characters
            if characters == '"':
                self.is_quote = not self.is_quote
                if self.is_quote == False:
                    self.stats_array.append(self.current_card_stats)
                    self.current_card_stats = ""
    
    def choose_card(self):
        biggest = -100000
        place = 0
        self.already_done.append(self.current_card)
        if len(self.already_done) == len(self.cards_array) - 1:
            self.already_done.popleft()
        for cards in range(len(self.cards_array)):
            can_be = True
            current = self.stats_array[cards]
            temp_nr = current.find("NR")
            next_recall = int(current[temp_nr+2:])
            if cards in self.already_done:
                can_be = False
            elif next_recall > biggest and can_be == True:
                biggest = next_recall
                place = cards
        self.current_card = place        

    def get_front(self):
        self.is_quote = False
        self.is_hashtag = False
        self.front_card_text = ""
        self.whole_card = self.cards_array[self.current_card]
        for characters in self.whole_card:
            if characters == "#":
                self.hashtag_count = self.hashtag_count + 1
                if self.hashtag_count == 2:
                    self.front_card_text = self.front_card_text + characters
                    self.front_card_text = self.front_card_text.replace("##","")
                    self.is_hashtag = not self.is_hashtag
                    self.hashtag_count = 0
            if self.is_hashtag == False:
                self.front_card_text = self.front_card_text + characters
        return self.front_card_text
        # Logic to get the front of the flashcard

    def get_back(self):
        self.is_quote = False
        self.is_hashtag = False
        self.back_card_text = ""
        self.whole_card = self.cards_array[self.current_card]
        for characters in self.whole_card:
            if self.is_hashtag == True:
                self.back_card_text = self.back_card_text + characters
                self.hashtag_count = 0
            if characters == "#":
                self.hashtag_count = self.hashtag_count + 1
                if self.hashtag_count == 2:
                    self.is_hashtag = not self.is_hashtag
                    self.hashtag_count = 0
        return self.back_card_text
        # Logic to get the back of the flashcard
    
    def card_running_system(self, button):
        self.difficulty = button
        self.old_stats = self.stats_array[self.current_card]
        self.current_card_stats = self.stats_array[self.current_card]
        temp_as = self.current_card_stats.find("AS")
        temp_tr = self.current_card_stats.find("TR")
        temp_nr = self.current_card_stats.find("NR")

        self.accuracy_score = int(self.current_card_stats[temp_as+2:temp_tr])
        self.times_recalled = int(self.current_card_stats[temp_tr+2:temp_nr])
        self.next_recall = int(self.current_card_stats[temp_nr+2:])
        # Handle updating accuracy scores and recall times
        if self.difficulty == "Easy": 
            self.accuracy_score = self.accuracy_score + 1 
            self.times_recalled = self.times_recalled + 1
            if self.accuracy_score < 0:
                self.accuracy_score = 0
        if self.difficulty == "Managed": 
            self.accuracy_score = self.accuracy_score - 1
        if self.difficulty == "Challenge":
            self.accuracy_score = self.accuracy_score - 2
            self.times_recalled = self.times_recalled + 1
        self.memory_calculator()
        self.scores_update()
        self.choose_card()
        self.update_file()
        if self.improvements_required == True:
            self.answer_frame.place_forget()
            self.improvements_frame.place(x=0,y=0)
            self.improvements_required = False
        else:
            self.show_front()

    def update_file(self):
        file = open("Flashcard file.txt","r")
        old_line = file.readline(self.current_card)
        file.close()
        file = open("Flashcard file.txt", "r")
        whole_file = file.read()
        file.close()
        new_stats = self.stats_array[self.current_card]
        new_line = old_line.replace(self.old_stats,new_stats)
        whole_file = whole_file.replace(old_line,new_line)
        file = open("Flashcard file.txt","w")
        file.write(whole_file)
        file.close()

    def scores_update(self):
        temp_stats = self.current_card_stats
        temp_as = self.current_card_stats.find("AS")
        temp_tr = self.current_card_stats.find("TR")
        temp_nr = self.current_card_stats.find("NR")

        temp_replace_as = str("AS" + self.current_card_stats[temp_as+2:temp_tr])
        temp_stats = temp_stats.replace(temp_replace_as,"")

        temp_replace_tr = str("TR" + self.current_card_stats[temp_tr+2:temp_nr])
        temp_stats = temp_stats.replace(temp_replace_tr,"")

        temp_replace_nr = str("NR" + self.current_card_stats[temp_nr+2:])

        self.current_card_stats = self.current_card_stats.replace(temp_replace_as,"AS" + str(self.accuracy_score))
        self.current_card_stats = self.current_card_stats.replace(temp_replace_tr,"TR" + str(self.times_recalled))
        self.current_card_stats = self.current_card_stats.replace(temp_replace_nr,"NR" + str(self.next_recall))

        self.stats_array[self.current_card] = self.current_card_stats
        
    def memory_calculator(self):
        self.next_recall = 0
        if self.times_recalled > 3:
            if self.accuracy_score < -4:
                self.improvements_required = True
        if self.times_recalled >= 3: 
            if self.accuracy_score >= 4:
                self.accuracy_score = self.accuracy_score - 1
                self.next_recall = -(round((self.accuracy_score + (self.accuracy_score*0.5))))
            if self.accuracy_score == 3:
                self.next_recall = 0
            if self.accuracy_score == 2: 
                self.next_recall = 0 
            if self.accuracy_score == 1: 
                self.next_recall = 1 
            if self.accuracy_score == 0: 
                self.next_recall = 1 
            if self.accuracy_score == -1: 
                self.next_recall = 3 
            if self.accuracy_score == -2: 
                self.next_recall = 3 
            if self.accuracy_score == -3: 
                self.next_recall = 5 
            if self.accuracy_score == -4: 
                self.next_recall = 7 
            if self.accuracy_score <= -5:
                improvements_required = True
                temp_accuracy = self.accuracy_score * -1 
                temp_accuracy = math.floor((temp_accuracy + 2) * 1.25) 
                self.next_recall = temp_accuracy 
        if self.times_recalled == 2:  
            if self.accuracy_score == 2: 
                self.next_recall = 0 
            if self.accuracy_score == 1: 
                self.next_recall = 1 
            if self.accuracy_score == 0: 
                self.next_recall = 1 
            if self.accuracy_score == -1: 
                self.next_recall = 2 
            if self.accuracy_score == -2: 
                self.next_recall = 2 
            if self.accuracy_score == -3: 
                self.next_recall = 3 
            if self.accuracy_score <= -4:
                temp_accuracy = self.accuracy_score * -1
                temp_accuracy = math.floor((temp_accuracy + 1) * 1.5) 
                self.next_recall = temp_accuracy
        if self.times_recalled == 1: 
            if self.accuracy_score == 1: 
                self.next_recall = 0 
            if self.accuracy_score == -1: 
                self.next_recall = 1 
            if self.accuracy_score == -2: 
                self.next_recall = 2

    def show_back(self):
        self.question_frame.place_forget()
        self.improvements_frame.place_forget()
        self.answer_frame.place(x=0,y=0)
        self.back_card_answer.configure(text=self.get_front() + " ➝ " + self.get_back())
        # Show the back of the flashcard

    def show_front(self):
        self.answer_frame.place_forget()
        self.improvements_frame.place_forget()
        self.question_frame.place(x=0,y=0)
        self.front_card_question.configure(text=self.get_front()+ " ➝ ?")

os.chdir("./File folder//Flashcard folder/")
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.title("Application")
    root.geometry("1100x600")
    root.config(background="dark grey")
    root.mainloop()
