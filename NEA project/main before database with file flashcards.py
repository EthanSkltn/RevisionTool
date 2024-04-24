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

root.title("Application")

os.chdir("./File folder/")

def clear_window():
        frames = [root]
        for frame in frames:
            for widget in frame.winfo_children():
                widget.destroy()
#A recursive function to gather all file names in a directory



class Interface:
    def __init__(self, master, screen_width, screen_height, username, user_id):
        self.user_id = user_id
        self.master = master
        self.username = username
        clear_window()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.main_directory = os.getcwd()

        self.directory = ""
        self.displayed = []
        self.newy = 20
        self.setup_ui()
        self.get_all_files("User files")
        self.create_file_buttons()
        
    def setup_ui(self):
        self.master.title("Application")
        self.master.geometry("1920x1080")
        self.master.state("zoomed")

        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")

        self.create_frames()
        self.create_widgets()

    def create_frames(self):
        self.frame3 = customtkinter.CTkFrame(self.master, width=(5/32)*self.screen_width, height=self.screen_height)
        self.frame3.place(x=0, y=-1)

        self.frame2 = customtkinter.CTkFrame(self.master, width=(14/16)*self.screen_width, height=(5/32)*self.screen_height)
        self.frame2.place(x=(5/32)*self.screen_width+3, y=0)

        self.frame1 = customtkinter.CTkFrame(self.master, width=(107.7/128)*self.screen_width, height=(29/32)*self.screen_height)
        self.frame1.place(x=(5/32)*self.screen_width+3, y=(11/64)*self.screen_height)

        self.frame_document_area = customtkinter.CTkFrame(self.frame3, width=(5/32)*self.screen_width-2, height=1000)
        self.frame_document_area.place(x=1, y=(5/16)*self.screen_height)

        self.account_frame = customtkinter.CTkFrame(self.frame3, width=(5/32)*self.screen_width-1)
        self.account_frame.place(x=1,y=1)

    def create_widgets(self):
        self.account_label = customtkinter.CTkLabel(self.account_frame,text = self.username)
        self.account_label.place(x=2,y=4)

        self.practice_flashcards = customtkinter.CTkButton(self.frame3,text="Practice flashcards",command=self.flashcard_practice)
        self.practice_flashcards.place(x=10,y=380)
        
        self.document_create_button = customtkinter.CTkButton(self.frame3, text="+", width=30, height=30, command=self.create_file)
        self.document_create_button.place(x=220, y=453)

        self.my_entry1 = customtkinter.CTkEntry(self.frame1, width=700, font=("Helvetica", 50))
        self.my_entry1.place(x=50, y=20)

        self.frame_my_text1 = customtkinter.CTkFrame(self.frame1, width=(11/16)*self.screen_width+15, height=(20/32)*self.screen_height)
        self.frame_my_text1.place(x=50, y=110)

        self.my_text1 = customtkinter.CTkTextbox(self.frame_my_text1, font=("Helvetica", 20), width=(11/16)*self.screen_width, height=(20/32)*self.screen_height)
        self.my_text1.place(x=0, y=0)

        self.frame_textsize = customtkinter.CTkFrame(self.frame2, width=80, height=40, border_width=1)
        self.frame_textsize.place(x=500, y=15)

        self.label_list = customtkinter.CTkLabel(self.frame_textsize, text="Font size")
        self.label_list.pack(padx=10, pady=5)

        self.text_slider_1 = customtkinter.CTkSlider(master=self.frame_textsize, command=self.update_textsize, from_=5, to=30)
        self.text_slider_1.pack(pady=10, padx=10)

        self.button_create_folder = customtkinter.CTkButton(self.frame2, text="Create folder", command=self.createFolder, height=1, width=15)
        self.button_create_folder.place(x=300, y=20)

        self.save_button = customtkinter.CTkButton(self.frame2, text="Save File", command=self.save_txt)
        self.save_button.place(x=10, y=50)

        self.load_all_files_button = customtkinter.CTkButton(self.frame3, text="Get all files", command=partial(self.get_all_files ,"User files"))
        self.load_all_files_button.place(x=10,y=350)

        self.flashcard_system_button = customtkinter.CTkButton(self.frame3,text="Create flashcards!",command=self.run_flashcard_system)
        self.flashcard_system_button.place(x=10,y=200)

    def run_flashcard_system(self):
        self.save_txt()
        self.my_entry1.delete(0,END)
        self.my_text1.delete(0.0, END)
        self.my_entry1.insert(END,"Flashcards")
        os.chdir(self.main_directory)
        Flashcard_System(root,self.user_id,self.username,self.my_text1)


    def flashcard_practice(self):
        FlashcardApp(root,self.user_id,self.username,self.main_directory)

    def create_file_buttons(self):
        for file in range(len(self.displayed)):
            temp = str(self.displayed[file])
            temp = temp.replace(".txt","", -1)
            second = temp
            temp = customtkinter.CTkButton(
                self.frame_document_area, width = 200,
                  text=temp,command=partial(self.open_txt, temp)
                  )
            temp.place(x=15,y=100+self.newy)
            if second == "User files":
                temp.place_forget()
                self.newy = self.newy - 40
            self.newy= self.newy + 35

    def get_all_files(self, folder_name):
        #Reset of all values which will count number of files and folders
        file_count = 0
        next_file = ""
        folder_name = str(folder_name + "\*")
        #Loops through the files given by next file
        for files in glob.glob(folder_name):
            #Identifies wether there is multiple files in a self.directory and if not it means it is a file or empty folder
            file_count = file_count + 1
            #IF statment acting as a base case and identifier
            if file_count >= 1:
                next_file = files
                self.get_all_files(next_file)
                #After return it will run a function to display the files
                name = next_file
                slash_count = 0
                startpoint = 0
                name_len = int(len(name))
                #This loops through all characters in the current name
                for character in range(name_len+1):
                    #This get the character of the current position in loop and if it is a "/" a function is performed
                    position = name[character-1]
                    if position == "\\" or character == name_len:
                        #This identifies how many folders the folder or files is in previously
                        slash_count = slash_count + 1
                        #Gets the name of the self.directory the folder is within
                        self.directory = name[startpoint : character : 1]
                        #Resetting the point at which the next self.directory name will start from
                        startpoint = character
                        #This clears up the left over backslashes
                        self.directory = self.directory.replace("\\","")
                        #Offloading the self.directory name to another function which will create a list of files on the user interface
                        self.displayed.append(self.directory)
            #IF file or empty folder it returns
            else:
                return
        print(self.displayed)
    
    def create_file(self):
        os.chdir(self.main_directory)
        os.chdir("./User files/")
        can_create = True
        text_file = str(self.my_entry1.get())
        if text_file != "":
            for file in glob.glob("*.txt"):
                if file == (text_file + ".txt"):
                    print("File already exists in this folder.")
                    can_create = False
            if can_create == True:
                file = open(text_file + ".txt", 'w')
                file.write(self.my_text1.get(1.0, END))
                file.close()
                #save the file
        self.create_file_buttons()
     
    def open_txt(self, text_file):
        os.chdir(self.main_directory)
        os.chdir("./User files/")
        self.save_txt()
        self.my_entry1.delete(0,END)
        self.my_text1.delete(0.0, END)
        #This part removes the current text from the text box and entry box
        if text_file != "":
            text_file = text_file + ".txt"
            file = open(text_file, 'r')
            stuff = file.read()
            self.my_text1.insert(END, stuff)
            #This inserts the file opened into the text box.
            file.close()
            text_file = str(text_file).replace(".txt", "")
            self.my_entry1.insert(END, text_file)
        #To maintain the current self.directory it returns it so other folders can be accessed

    def save_txt(self):
        os.chdir(self.main_directory)
        os.chdir("./User files/")
        text_file = str(self.my_entry1.get() + ".txt")
        text_file = open(text_file, 'w')
        text_file.write(str(self.my_text1.get(0.0, END)))
        text_file.close()

#This function overrides the previous file contents as it uses the write command

    def createFolder(self):
        directory = str(self.my_entry1.get())
        directory = str("./" + directory + "/")
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)

    def update_textsize(self, text_size):
        self.my_text1.configure(font=("Helvetica", text_size))

class Login_System:
    def __init__(self, root):
        self.user_id = ""
        self.dont_write = False
        self.access_granted = False
        self.can_create = False
        self.setup_ui(root)
        self.try_skip()

    def setup_ui(self, root):
        self.root = root
        self.entry_frame = Frame(root)
        self.entry_frame.pack()


        self.title = customtkinter.CTkLabel(self.entry_frame, text="Enter details")
        self.title.pack(anchor=NW,padx=20,pady=10)

        self.username_frame = customtkinter.CTkFrame(self.entry_frame)
        self.username_frame.pack(padx=10,pady=5)

        self.label_username = customtkinter.CTkLabel(self.username_frame,text="Username", font=("Helvetica",12))
        self.label_username.pack(anchor=W,padx=5,pady=1)

        self.username_entry = customtkinter.CTkEntry(self.username_frame, width=400, height=40, font=("Helvetica", 15))
        self.username_entry.pack()

        self.email_frame = customtkinter.CTkFrame(self.entry_frame)
        self.email_frame.pack(padx=10,pady=5)

        self.label_email = customtkinter.CTkLabel(self.email_frame,text="Email", font=("Helvetica",12))
        self.label_email.pack(anchor=W,padx=5,pady=1)

        self.email_entry = customtkinter.CTkEntry(self.email_frame, width=400, height=40, font=("Helvetica", 15))
        self.email_entry.pack()

        self.password_frame = customtkinter.CTkFrame(self.entry_frame)
        self.password_frame.pack(padx=10,pady=5)

        self.label_password = customtkinter.CTkLabel(self.password_frame,text="Password", font=("Helvetica",12))
        self.label_password.pack(anchor=W,padx=5,pady=1)

        self.password_entry = customtkinter.CTkEntry(self.password_frame, width=400, height=40, font=("Helvetica", 15))
        self.password_entry.pack()

        self.retry_frame = customtkinter.CTkFrame(self.password_frame,height=0,width=0)
        self.retry_frame.pack()

        self.enter_button = customtkinter.CTkButton(self.entry_frame,text="Enter", command=self.validate)
        self.enter_button.pack(pady=5,padx=20,anchor=SE)

        self.create_button = customtkinter.CTkButton(self.entry_frame,text="Create account", command=self.create_account)
        self.create_button.pack(pady=5,padx=20,anchor=SE)

        self.retry_username = customtkinter.CTkLabel(self.retry_frame,text="Incorrect username entered!",font=("Helvetica", 12))

        self.retry_password = customtkinter.CTkLabel(self.retry_frame,text="Incorrect password entered!",font=("Helvetica", 12))

        self.retry_email = customtkinter.CTkLabel(self.retry_frame,text="Incorrect email entered!",font=("Helvetica", 12))

    def fetch_user_info(self):
        cursor = connection.cursor()
        self.username = self.username_entry.get()
        self.information = cursor.execute("""SELECT account_id, email, password
                          FROM Accounts
                                     WHERE username = ?""",self.username).fetchone()

    def validate(self):
        user_failed = 0
        pass_failed = 0
        self.retry_frame.pack()
        self.fetch_user_info()
        if self.username != "":
            try:
                self.user_id = self.information[0]
                self.user_email = self.information[1]
                self.user_password = self.information[2]
                self.retry_username.pack_forget()
                if self.email_entry.get() == self.user_email:
                    self.retry_email.pack_forget()
                    if self.password_entry.get() == self.user_password:
                        self.retry_password.pack_forget()
                        self.retry_frame.pack_forget()
                        print("Correct entry")
                        self.access_granted = True
                    else:
                        self.retry_password.pack_forget()
                        self.retry_password.pack(anchor="w",pady=2)
                        print("Password is Incorrect")
                else:
                    if pass_failed == 0:
                        self.retry_email.pack_forget
                        self.retry_email.pack(anchor="w",pady=2)
                        print("Email is incorrect")
                    pass_failed = pass_failed + 1
            except:
                if user_failed == 0:
                    self.retry_username.pack_forget()
                    self.retry_username.pack(anchor="w",pady=2)
                    print("Account does not exist")
                user_failed = user_failed + 1
            self.login_complete()

    def create_account(self):
        self.information = cursor.execute("""SELECT username, email, password, account_id
                          FROM Accounts""").fetchall()
        char = 0
        ats = 0
        dots = 0
        upper = 0
        numbers = 0
        next_id = int(self.information[(len(self.information))-1][3]) + 1

        for i in range(len(self.information)):
            if self.information[i][0] == self.username_entry.get():
                self.can_create = False
            if len(self.information[i][0]) < 5:
                self.can_create = False
            else:
                self.can_create = True

        for i in range(len(self.information)):
            if self.information[i][1] == self.email_entry.get():
                self.can_create = False
            if len(self.username_entry.get()) > 5:
                for characters in self.email_entry.get():
                    if characters == "@":
                        ats = ats+ 1
                    elif characters == ".":
                        if ats == 1:
                            dots = dots + 1
                    else:
                        char = char + 1
                if ats == 1 and dots > 0 and char > 10:
                    self.can_create = True
                else:
                    self.can_create = False
            else:
                self.can_create = False
        
    
        if len(self.password_entry.get()) > 8:
                    for characters in self.password_entry.get():
                        if characters.isupper() == True:
                            upper = upper + 1
                        if characters.isnumeric():
                            numbers = numbers + 1
                    if numbers > 0 and upper > 0:
                        self.can_create = True
                    else:
                        self.can_create = False
        else:
            self.can_create = False
        if self.can_create == True:
            data = (str(self.username_entry.get()),str(self.password_entry.get()),str(self.email_entry.get()),int(next_id))
            cursor.execute("""INSERT INTO Accounts (username,password,email,account_id)
                           VALUES (?,?,?,?)""",data)
            self.user_id = next_id
            connection.commit()
            print("Created")
            self.login_complete()

    def try_skip(self):
        file = open("Skip login.txt","r")
        lines = file.read()

        self.information = cursor.execute("""SELECT username, email, password, account_id
                          FROM Accounts""").fetchall()
        for rows in range(len(self.information)):
            if lines == self.information[rows][0] + self.information[rows][1] + self.information[rows][2]:
                self.row_line = rows
                self.dont_write = True
                time.sleep(1)
                self.current_id = self.information[rows][3]
                self.login_complete()

    def login_complete(self):
        if self.dont_write != True:
            self.username = self.username_entry.get()
            file = open("Skip login.txt","w")
            put_in = self.username + self.email_entry.get() + self.password_entry.get()
            file.write(str(put_in))
            file.close()
        else:
            self.username = self.information[self.row_line][0]
        Interface(self.root, width, height, self.username, self.user_id)

class FlashcardApp:
    def __init__(self, root, username, user_id, main_directory):
        self.main_directory = main_directory
        self.username = username
        self.user_id = user_id
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
        
        clear_window()
        os.chdir(self.main_directory)
        os.chdir("./Flashcard folder/")
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

        self.exit_button = customtkinter.CTkButton(root,text="X",command=self.exit_cards,corner_radius=1, width=20,height=30)
        self.exit_button.place(x=1000,y=10)

    def exit_cards(self):
        os.chdir(self.main_directory)
        Interface(root,width,height,self.username,self.user_id)

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

class Flashcard_System:
    def __init__ (self,root, user_id, username,my_text1):
        os.chdir("./Flashcard folder/")
        self.username = username
        self.user_id = user_id

        self.confirm_card = customtkinter.CTkButton(root,text="Confirm cards",command = self.load_flashcards)
        self.confirm_card.place(x=1250,y=220)
        self.my_text1 = my_text1
        
        self.cards_array = []
        self.whole_card = ""
        self.card_front = ""

        self.load_existing_cards()
        self.count = self.my_text1.bind("<Key>", self.count_flashcards)
    
    def load_existing_cards(self):
        file = open("Flashcard file.txt","r")
        self.whole_card = file.read()
        file.close()
        self.is_quote = False
        for characters in self.whole_card:
            if self.is_quote == True and characters != '"':
                self.card_front = self.card_front + characters
            if characters == '"':
                self.is_quote = not self.is_quote
                if self.is_quote == False:
                    self.card_front = self.card_front.replace("##","➝")
                    self.my_text1.insert(END,self.card_front+"\n")
                    self.card_front = ""
        print(self.cards_array)

    def front_card(self,lines):
        #the list which will be returned to the primary function to input into the file
        card_front = []
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
                        card_front.append(text_list[i-2])
        #returns the list of characters in the front of the card
        return card_front

    def back_card(self,lines):
        #the list which will be returned to the primary function to input into the file
        card_back = [""]
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
                            elif text_list[i] == '"':
                                card_back.append("'")
                            else:
                                card_back.append(text_list[i])
        #returns the list of characters in the front of the card
        return card_back

    def load_flashcards(self):
        #lines is a variable which indicates the line number of the flashcard
        lines = 0
        #to clear the file of repeats before writting the flashcards in
        file = open("Flashcard file.txt","w").close()
        #a loop to distinguish the characters require to create the card
        for letter in self.my_text1.get(0.0,END):
            #if there is a new line the lines count goes up 1
            if letter == "\n":
                lines = lines + 1
            #if there is a "➝" it enters the card creation
            if letter == "➝":
                #entering the front of card function with the current line position
                extract = self.front_card(lines)
                #this opens the file in append mode and adds on to the end of the file the front of the card
                file = open("Flashcard file.txt", "a")
                file.write('AS0TR0NR0')
                file.write('"')
                for fronts in range(len(extract)):
                    file.write(extract[fronts])
                #to distinguish between front and back of card in the file
                file.write("##")
                #enters the back card creation function and appends to the end of the opened file
                back = self.back_card(lines)
                for fronts in range(len(back)):
                    file.write(back[fronts])
                file.write('"')
                file.write("\n")
                #this closes the file
                file.close()

    #This function is the function trigured when the flashcard command is typed "##"
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
     
login_system1 = Interface(root,width,height,"Ethan",1)
root.mainloop()
#this is how the window loops itself