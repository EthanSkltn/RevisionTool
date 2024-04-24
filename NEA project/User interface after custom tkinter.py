from tkinter import *
from tkinter import filedialog
import os, glob
import customtkinter
from functools import partial
import pyodbc
#the imports of tkinter libraries.
root = Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue") 

root.title("Application")
root.geometry("1920x1080")
root.state("zoomed")
#this opens the window in a windowed full screen state.

folder_name = "Text files"
folder_count = 0

connection = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-9PT14TH;'
    'Database=NEA project;'
    'Trusted_Connection=yes;'
)

cursor = connection.cursor() 


information = cursor.execute("""SELECT account_id, username, email, password
                          FROM Accounts""").fetchall()
    
print(information)
os.chdir("./File folder/")       

#A recursive function to gather all file names in a self.directory


class interface:
    def __init__(self, master, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.master = master
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
        self.frame_document_area.place(x=1, y=(3/16)*self.screen_height)

    def create_widgets(self):
        self.document_create_button = customtkinter.CTkButton(self.frame3, text="Created document", width=60, height=30, command=self.create_file)
        self.document_create_button.place(x=15, y=10)

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
        self.load_all_files_button.place(x=10,y=70)
    
    def create_file_buttons(self):
        for file in range(len(self.displayed)):
            temp = str(self.displayed[file])
            temp = temp.replace(".txt","", -1)
            second = temp
            temp = customtkinter.CTkButton(self.frame_document_area, width = 200, text=temp,command=partial(self.open_txt, temp))
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

    
# Example

interface1 = interface(root, width, height)

root.mainloop()
