from tkinter import *
import tkinter as tk
import os
import customtkinter
from functools import partial
from collections import deque
import math
import pyodbc
import hashlib
from PIL import  Image, ImageTk
from spellchecker import SpellChecker

# Color themes
colour_theme1 = "#6BBF90"  # Define color theme 1
colour_theme2 = "#B0D9C1"  # Define color theme 2
colour_theme3 = "#D9BCA3"  # Define color theme 3

# Alternative color themes
# colour_theme1 = "#949294"
# colour_theme2 = "#decedb"
# colour_theme3 = "#ffffff"

# Create the root tkinter window
root = Tk()
root.attributes('-fullscreen', True)
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue") 

root.title("Application")
root.configure(background=colour_theme2)

def clear_window():
    """
    Clear all widgets from the root window.

    This function destroys all widgets in the root window, effectively clearing the window.
    """
    frames = [root]
    for frame in frames:
        for widget in frame.winfo_children():
            widget.destroy()

def line_making(text, characters_long):
    """
    Format text to have line breaks at specified character count.

    Args:
        text (str): The input text to format.
        characters_long (int): The maximum number of characters before a line break.

    Returns:
        str: The formatted text with line breaks.

    This function adds line breaks to the text so that no line contains more than the specified number of characters.
    """
    i = 0
    previous_word = 0
    for j in range(len(text)):
        i = i + 1
        if text[j] == " ":
            previous_word = j
        if text[j] == "\n":
            i = 0
        if i == characters_long:
            if i - previous_word > 15:
                previous_word = j
            start = text[:previous_word]
            end = text[previous_word:]
            text = start + "\n" + end
            i = 0
    return text

# Establish a connection to the database
connection = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=ETHANS-LAPTOP;'
    'Database=NEA project;'
    'Trusted_Connection=yes;'
)
cursor = connection.cursor()

# Load and resize images
delete_image_pil = Image.open("Delete image.png")
delete_image_pil_resized = delete_image_pil.resize((20, 20), Image.LANCZOS)
delete_image = ImageTk.PhotoImage(delete_image_pil_resized)

home_image_pil = Image.open("Home image.jpg")
home_image_resized = home_image_pil.resize((20, 20), Image.LANCZOS)
home_image = ImageTk.PhotoImage(home_image_resized)

setting_image_pil = Image.open("Settings image.png")
setting_image_resized = setting_image_pil.resize((20, 20), Image.LANCZOS)
setting_image = ImageTk.PhotoImage(setting_image_resized)

# Change the current directory to the "File folder" directory
os.chdir("./File folder/")

class HomeScreen:
    """
    HomeScreen class for the main user interface.

    This class represents the home screen of the application, where the user can access different features.

    Args:
        user_id (int): The user's ID.
        username (str): The username of the user.

    Attributes:
        user_id (int): The user's ID.
        username (str): The username of the user.

    Methods:
        setup_ui: Sets up the user interface elements.
        run_flashcard_app: Opens the flashcard creation and editing app.
        practice_flashcard_app: Opens the flashcard practice app.
        run_files: Opens the file management interface.
        practice_exam_app: Opens the exam question practice app.
    """

    def __init__(self, user_id, username):
        """
        Initialize a HomeScreen instance.

        Args:
            user_id (int): The user's ID.
            username (str): The username of the user.
        """
        clear_window()
        self.user_id = user_id
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface elements.
        """
        self.close_button = customtkinter.CTkButton(
            root,
            text="Close app",
            command=root.quit,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3
        )
        self.close_button.place(x=1300, y=10)

        self.button_frame = customtkinter.CTkFrame(root, 
                                                   fg_color=colour_theme2
        )
        
        self.button_frame.pack(pady=100)

        self.flashcard_practice = customtkinter.CTkButton(
            self.button_frame,
            text="Practice your flashcards",
            font=("Helvetica", 25),
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            width=600,
            height=300,
            command=self.practice_flashcard_app
        )
        self.flashcard_practice.grid(column=1, row=0, padx=5, pady=5)

        self.flashcard_editting = customtkinter.CTkButton(
            self.button_frame,
            text="Create and edit your flashcards",
            font=("Helvetica", 25),
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            width=600,
            height=300,
            command=self.run_flashcard_app
        )
        self.flashcard_editting.grid(column=0, row=1, padx=5, pady=5)

        self.files = customtkinter.CTkButton(
            self.button_frame,
            text="Create and add to your files",
            font=("Helvetica", 25),
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            width=600,
            height=300,
            command=self.run_files
        )
        self.files.grid(column=1, row=1, padx=5, pady=5)

        self.practice_exam_questions = customtkinter.CTkButton(
            self.button_frame,
            text="Practice subject-specific exam questions",
            font=("Helvetica", 25),
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            width=600,
            height=300,
            command=self.practice_exam_app
        )
        self.practice_exam_questions.grid(column=0, row=0, padx=5, pady=5)

    def run_flashcard_app(self):
        """
        Open the flashcard creation and editing app.
        """
        Flashcard_System(root, self.user_id, self.username)

    def practice_flashcard_app(self):
        """
        Open the flashcard practice app.
        """
        FlashcardApp(root, self.username, self.user_id)

    def run_files(self):
        """
        Open the file management interface.
        """
        Interface(root, width, height, self.username, self.user_id)

    def practice_exam_app(self):
        """
        Open the exam question practice app.
        """
        ExamQuestion(self.user_id, self.username)


class Interface:
    def __init__(self, master, screen_width, screen_height, username, user_id):
        """
        Initialize the Interface class.

        Args:
            master (tkinter.Tk): The root tkinter window.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            username (str): The username of the user.
            user_id (int): The user's unique ID.

        This constructor initializes the Interface class and sets up initial attributes.
        """
        self.user_id = user_id
        self.master = master
        self.username = username

        # Clear the current window to start with a clean slate
        clear_window()

        # Inputed height and width (int) to give a ratio for the program
        self.screen_width = screen_width
        self.screen_height = screen_height


        # Lists to store directory and file information.
        self.all_directories = []
        self.all_files = []
        self.file_id_array = []
        self.folder_id_array = []

        # Position attributes for file and folder creation.
        self.xpad = 5
        self.ypad = 0

        # Current folder and file being edited.
        self.current_folder = 0
        self.current_file = 0

        # Initialize a SpellChecker for spelling correction.
        self.spell = SpellChecker()

        # Set up the user interface.
        self.setup_ui()

        
        # Fetch all files and create buttons for them.
        self.get_all_files()
        self.create_file_buttons()
        self.my_text1.bind(self.save_txt)

    def setup_ui(self):
        """
        Set up the user interface for the main application window.

        This method configures the appearance and layout of the main application window.
        """
        self.master.title("Application")
        self.master.geometry("1920x1080")
        self.master.state("zoomed")

        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")

        self.create_frames()
        self.create_widgets()

    def create_frames(self):
        """
        Create and place custom frames within the main window.

        This method creates and positions custom frames for various sections of the main window.
        """
        self.frame3 = customtkinter.CTkFrame(
            self.master,
            fg_color=colour_theme1,
            width=(5/32)*self.screen_width,
            height=self.screen_height,
            border_color=colour_theme2,
            border_width=3
        )
        self.frame3.place(x=0, y=-1)

        self.frame2 = customtkinter.CTkFrame(
            self.master,
            fg_color=colour_theme1,
            width=(14/16)*self.screen_width,
            height=(5/32)*self.screen_height,
            border_color=colour_theme2,
            border_width=3
        )
        self.frame2.place(x=(5/32)*self.screen_width+3, y=0)

        self.frame1 = customtkinter.CTkFrame(
            self.master,
            fg_color=colour_theme2,
            width=(107.7/128)*self.screen_width,
            height=(29/32)*self.screen_height
        )
        self.frame1.place(x=(5/32)*self.screen_width+3,
                           y=(11/64)*self.screen_height
        )

        self.frame_document_area = Canvas(
            self.frame3,
            width=150,
            height=800,
            background=colour_theme1
        )
        self.frame_document_area.place(x=1, y=(5/16)*self.screen_height)

        self.account_frame = customtkinter.CTkFrame(
            self.frame3,
            fg_color=colour_theme1,
            width=(4.5/32)*self.screen_width-1,
            border_color=colour_theme2,
            border_width=3
        )
        self.account_frame.place(x=10, y=1)

        self.settings_frame = customtkinter.CTkFrame(
            root,
            fg_color=colour_theme2,
            border_color=colour_theme1,
            border_width=3,
            height=700,
            width=1000
        )

        self.directory_create_frame = customtkinter.CTkFrame(
            root,
            fg_color=colour_theme2,
            border_color=colour_theme1,
            border_width=3,
            height=200,
            width=500
        )

    def create_widgets(self):
        """
        Create and place custom widgets within the main window and frames.

        This method creates and positions custom widgets, buttons, and other UI elements within the main window.
        """
        self.account_label = customtkinter.CTkLabel(
            self.account_frame,
            text_color=colour_theme3,
            text=self.username
        )
        self.account_label.place(x=70, y=10)

        self.home_button = customtkinter.CTkButton(
            self.account_frame,
            width=50,
            height=50,
            text="",
            border_color=colour_theme2,
            border_width=3,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            image=home_image,
            command=self.run_home
        )
        self.home_button.place(x=10, y=10)

        self.settings_button = customtkinter.CTkButton(
            self.account_frame,
            width=50,
            height=50,
            text="",
            border_color=colour_theme2,
            border_width=3,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            image=setting_image,
            command=self.open_settings
        )
        self.settings_button.place(x=10, y=70)

        self.document_create_button = customtkinter.CTkButton(
            self.frame3,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            text="+",
            width=30,
            height=30,
            command=self.new_file
        )
        self.document_create_button.place(x=220, y=230)

        self.my_entry1 = customtkinter.CTkEntry(
            self.frame1,
            fg_color=colour_theme2,
            border_color=colour_theme1,
            border_width=3,
            width=700,
            font=("Helvetica", 50)
        )
        self.my_entry1.place(x=50, y=20)

        self.my_text1 = customtkinter.CTkTextbox(
            self.frame1,
            fg_color=colour_theme2,
            border_color=colour_theme1,
            border_width=3,
            font=("Helvetica", 20),
            width=(12/16)*self.screen_width,
            height=(20/32)*self.screen_height
        )
        self.my_text1.place(x=50, y=110)

        self.frame_textsize = customtkinter.CTkFrame(
            self.frame2,
            fg_color=colour_theme1,
            width=80,
            height=40,
            border_color=colour_theme2,
            border_width=3
        )
        self.frame_textsize.place(x=500, y=15)

        self.label_list = customtkinter.CTkLabel(
            self.frame_textsize,
            text_color=colour_theme3,
            text="Font size"
        )
        self.label_list.pack(padx=10, pady=5)

        self.text_slider_1 = customtkinter.CTkSlider(
            master=self.frame_textsize,
            progress_color=colour_theme1,
            fg_color=colour_theme1,
            bg_color=colour_theme2,
            button_color=colour_theme3,
            command=self.update_textsize,
            from_=5,
            to=30
        )
        self.text_slider_1.pack(pady=10, padx=10)

        self.button_create_folder = customtkinter.CTkButton(
            self.frame2,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            text="Create folder",
            command=self.run_folder_creation,
            height=1,
            width=15
        )
        self.button_create_folder.place(x=300, y=20)

        self.save_button = customtkinter.CTkButton(
            self.frame2,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            text="Save File",
            command=self.save_txt
        )
        self.save_button.place(x=10, y=50)

        self.load_all_files_button = customtkinter.CTkButton(
            self.frame3,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            text="Get all files",
            command=partial(self.get_all_files)
        )
        self.load_all_files_button.place(x=10, y=150)

        self.directory_scrollbar = customtkinter.CTkScrollbar(
            self.frame_document_area,
            fg_color=colour_theme1,
            button_color=colour_theme2,
            button_hover_color=colour_theme2,
            command=self.frame_document_area.yview
        )
        self.directory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.frame_document_area.configure(
            yscrollcommand=self.directory_scrollbar.set
        )

        self.document_frame = customtkinter.CTkFrame(
            self.frame_document_area,
            fg_color=colour_theme1,
            height=800
        )
        self.frame_document_area.create_window((0, 0),
                                         window=self.document_frame,
                                           anchor=NW)

        self.document_frame.bind("<Configure>",
                                lambda e: self.frame_document_area.configure
                                    (
                                    scrollregion=self.frame_document_area.bbox(
                                        "all"
                                        )
                                    )
                                )

        self.document_frame.pack(fill=tk.BOTH, expand=True)

        self.enter_label = customtkinter.CTkLabel(
            self.directory_create_frame,
            text="Enter directory name:",
            text_color=colour_theme3
        )
        self.enter_label.pack()

        self.folder_name_entry = customtkinter.CTkEntry(
            self.directory_create_frame,
            fg_color=colour_theme2,
            border_color=colour_theme1,
            border_width=3,
            width=250,
            height=40
        )
        self.folder_name_entry.pack()

        self.cancel_create = customtkinter.CTkButton(
            self.directory_create_frame,
            text="Cancel",
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            command=partial(self.createFolder, True)
        )
        self.cancel_create.pack(pady=5, padx=10)

        self.confirm_dir = customtkinter.CTkButton(
            self.directory_create_frame,
            text="Create",
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            command=partial(self.createFolder, False)
        )
        self.confirm_dir.pack(pady=5, padx=10)

        self.file_frame = customtkinter.CTkFrame(
            self.master,
            fg_color=colour_theme2,
            width=(107.7/128)*self.screen_width,
            height=(29/32)*self.screen_height
        )

        self.add_file = customtkinter.CTkButton(
            self.file_frame,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            text="Create new file",
            command=self.new_file
        )

        self.my_text1.bind("<KeyRelease>", self.check_spelling)

    def check_spelling(self,event):
        """
        Check and highlight misspelled words in the text.

        Args:
            event (tkinter.Event): The event that triggers the spelling check.

        This method checks the spelling of words in the text and highlights misspelled words with a red foreground.
        """
        if event.keysym == "space":
            self.my_text1.tag_remove("highlight", "1.0", "end")
            text = self.my_text1.get("1.0", "end")
            words = text.split()

            for word in words:
                print(word)
                if not self.spell.correction(word) == word:
                    self.highlight_word(word)

    def highlight_word(self, word):
        """
        Highlight occurrences of a word in the text.

        Args:
            word (str): The word to be highlighted in the text.

        This method finds and highlights all occurrences of the provided word in the text widget the sourced words will be misspelt words.

        It iterates through the text, searching for the word and adding a "highlight" tag to the found
        word, which makes it appear in red.

        Example:
        If `word` is "example," this method will find and highlight all instances of "example" in the text.
        """
        new_word = ""
        for char in word:
            if char.isalpha():
                new_word = new_word + char
        word = new_word
        start = "1.0"
        while start:
            start = self.my_text1.search(word, start, stopindex="end")
            if start:
                end = start + "+" + str(len(word)) + "c"
                self.my_text1.tag_add("highlight", start, end)
                start = end
        self.my_text1.tag_config("highlight", foreground="red")

    def setup_files(self, start_node):
        """
        Recursively create a hierarchical folder structure in the GUI.

        Args:
            start_node (int): The ID of the folder where the recursive structure starts.

        This method implements a depth-first algorithm to create a hierarchical folder structure in the GUI.
        It starts from the specified `start_node` and recursively explores the subfolders to create buttons
        representing each folder in the directory tree.

        The method performs the following steps:
        1. Increase the vertical position (ypad) to position the buttons vertically.
        2. Determine the name of the primary folder associated with the `start_node`.
        3. Create a button in the `document_frame` with the name of the primary folder.
        4. If subfolders exist within the primary folder, they are appended to the `nodes_inside` list.
        5. If there are subfolders, recursively call `setup_files` for each subfolder to continue exploring
        the directory structure.
        6. Adjust the horizontal position (xpad) to space out the buttons horizontally.

        This recursive algorithm creates buttons for each folder in a hierarchical structure, allowing users
        to navigate the directory tree.
        """
        self.ypad = self.ypad + 30
        primary = start_node
        primary_name = ""

        # Find the name of the primary folder
        for i in range(len(self.get_all_folders)):
            if self.get_all_folders[i][0] == primary:
                primary_name = self.get_all_folders[i][1]

        # Create a button for the primary folder
        button = customtkinter.CTkButton(
            self.document_frame,
            hover_color=colour_theme3,
            fg_color=colour_theme1,
            border_color=colour_theme2,
            border_width=3,
            text=primary_name,
            command=partial(self.open_folder, primary),
            width=150
        )
        button.place(x=self.xpad, y=self.ypad)

        nodes_inside = []

        # Find subfolders inside the primary folder
        for i in range(len(self.all_directories)):
            if self.all_directories[i][1] == None:
                pass
            else:
                if int(self.all_directories[i][1]) == int(primary):
                    nodes_inside.append(int(self.all_directories[i][0]))

        if len(nodes_inside) == 0:
            # If no subfolders, reduce horizontal position
            self.xpad = self.xpad - 10
            return
        else:
            # If subfolders exist, increase horizontal position and recurse
            self.xpad = self.xpad + 10
            for i in range(len(nodes_inside)):
                self.setup_files(nodes_inside[i])


    def setup_primary(self):
        """
        Set up the primary folder and initiate the creation of folder structure in the GUI.

        This method identifies the primary folder, which is the top-level directory, and starts the process
        of creating a hierarchical folder structure in the GUI by calling the `setup_files` method with
        the primary folder as the starting node.
        """
        for i in range(len(self.all_directories)):
            if self.all_directories[i][2] == "D" and self.all_directories[i][1] is None:
                primary = self.all_directories[i][0]
        self.setup_files(primary)

    def run_home(self):
        """
        Navigate to the home screen.

        This method creates an instance of the `HomeScreen` class to navigate back to the home screen of the application.
        """
        HomeScreen(self.user_id, self.username)

    def open_settings(self):
        """
        Open the settings screen.

        This method creates an instance of the `Settings` class to open the settings screen of the application.
        """
        Settings(self.user_id, self.username)

    def create_file_buttons(self):
        """
        Create file buttons and initiate the setup of the folder structure.

        This method initiates the setup of the folder structure by calling the `setup_primary` method.
        Additionally, this method is responsible for creating file buttons in the GUI.
        """
        self.setup_primary()

    def get_all_files(self):
        """
        Retrieve information about files and folders from the database.

        This method retrieves information about files and folders associated with the current user from the database.
        It populates the `all_file_info` and `get_all_folders` lists with relevant data.
        Additionally, it identifies primary folders and creates a list of all directories and file IDs.
        """
        self.all_file_info = cursor.execute("""
            SELECT file_name, file_id, file_contents, folder_id, account_id
            FROM Files
            WHERE account_id = ?
        """, self.user_id).fetchall()

        self.get_all_folders = cursor.execute("""
            SELECT folder_id, folder_name, directory_in_id, account_id
            FROM Folders
            WHERE account_id = ?
        """, self.user_id).fetchall()

        # Process folders and files data to create directory structure
        # and collect folder and file IDs.
        for i in range(len(self.get_all_folders)):
            if self.user_id == self.get_all_folders[i][3]:
                in_directory = self.get_all_folders[i][2]
                directory_id = self.get_all_folders[i][0]
                self.all_directories.append([directory_id, in_directory, "D"])

        for i in range(len(self.all_file_info)):
            if self.user_id == self.all_file_info[i][4]:
                in_directory = self.all_file_info[i][3]
                file_id = self.all_file_info[i][1]
                self.all_files.append([file_id, in_directory, "F"])

        # Collect folder and file IDs
        for i in range(len(self.get_all_folders)):
            self.folder_id_array.append(self.get_all_folders[i][0])

        for i in range(len(self.all_file_info)):
            self.file_id_array.append(self.all_file_info[i][1])

    def open_folder(self, folder_id):
        """
        Displaying the frame of folder attributes.

        Args:
            folder_id (int): The ID of the folder to be opened.
        """
        self.current_folder = folder_id
        self.frame1.place_forget()
        new_file_frame = customtkinter.CTkFrame(self.master, 
                                                fg_color=colour_theme2, 
                                                width=(107.7/128)*self.screen_width, 
                                                height=(29/32)*self.screen_height)
        delete_file_button = customtkinter.CTkButton(new_file_frame,
                                                    fg_color=colour_theme3, width=40,
                                                    height=40, image=delete_image,
                                                    text="",
                                                    command=partial(self.delete_folder, folder_id))
        delete_file_button.pack()
        self.add_file =  customtkinter.CTkButton(new_file_frame, hover_color=colour_theme1,
                                                text_color=colour_theme3, fg_color=colour_theme2,
                                                border_color=colour_theme1, border_width=3,
                                                text="Create new file", command=self.new_file)
        self.add_file.pack()
        for i in range(len(self.all_file_info)):
            if folder_id == self.all_file_info[i][3] and self.user_id == self.all_file_info[i][4]:
                button = customtkinter.CTkButton(new_file_frame, hover_color=colour_theme3,
                                                text_color=colour_theme1, fg_color=colour_theme2,
                                                border_color=colour_theme1, border_width=3,
                                                text=self.all_file_info[i][0], 
                                                command=partial(self.open_txt, self.all_file_info[i][1]))
                button.pack(pady=5)
        if hasattr(self, 'file_frame'):
            self.file_frame.place_forget()
            self.file_frame.destroy()
        self.file_frame = new_file_frame
        self.file_frame.place(x=(5/32)*self.screen_width+3, y=(11/64)*self.screen_height)
        self.add_file.pack()

    def delete_folder(self, folder_id):
        """
        Delete a folder and its contents from the GUI and database.

        Args:
            folder_id (int): The ID of the folder to be deleted.
        """
        self.delete_repeat(folder_id)
        clear_window()
        Interface(root, self.screen_width, self.screen_height, self.username, self.user_id)

    def delete_repeat(self, folder_id):
        """
        Recursively delete a folder and its contents from the GUI and database. Database requires files to be deleted in a depth first order.

        Args:
            folder_id (int): The ID of the folder to be deleted.
        """
        for i in range(len(self.get_all_folders)):
            if self.get_all_folders[i][2] == folder_id:
                self.delete_folder(self.get_all_folders[i][2])
        for i in range(len(self.all_file_info)):
            if self.all_file_info[i][3] == folder_id:
                cursor.execute("""DELETE FROM Files
                       WHERE file_id = ? AND folder_id = ? AND account_id = ?""",
                       self.all_file_info[i][1], folder_id, self.user_id)
                connection.commit()
        cursor.execute("""DELETE FROM Folders
                       WHERE folder_id = ? AND account_id = ?""", folder_id, self.user_id)
        connection.commit()

    def open_txt(self, file_id):
        """
        Open a text file for editing in the GUI.

        Args:
            file_id (int): The ID of the text file to be opened for editing.
        """
        name = ""
        contents = ""
        self.current_file = file_id
        self.frame1.place(x=(5/32)*self.screen_width+3, y=(11/64)*self.screen_height)
        self.my_entry1.delete(0, END)
        self.my_text1.delete(0.0, END)
        for i in range(len(self.all_file_info)):
            if self.current_folder == self.all_file_info[i][3] and self.user_id == self.all_file_info[i][4] and file_id == self.all_file_info[i][1]:
                contents = self.all_file_info[i][2]
                name = self.all_file_info[i][0]
        self.delete_file_button = customtkinter.CTkButton(self.frame1,
                                                          fg_color=colour_theme3,
                                                          width=40, height=40,
                                                          image=delete_image, text="",
                                                          command=self.delete_file)
        self.delete_file_button.place(x=800, y=30)
        self.file_frame.place_forget()
        self.my_entry1.insert(END, name)
        self.my_text1.insert(END, contents)

    def new_file(self):
        """
        Create a new text file in the GUI.

        This method creates a new empty text file for editing in the current folder.

        """
        self.frame1.place(x=(5/32)*self.screen_width+3, y=(11/64)*self.screen_height)
        self.my_entry1.delete(0, END)
        self.my_text1.delete(0.0, END)
        self.file_frame.place_forget()
        found = False
        i = 0
        contents = ""
        name = "New file"
        self.my_entry1.insert(END, name)
        while found == False:
            if i not in self.file_id_array:
                found = True
            else:
                i = i + 1
        self.current_file = i
        cursor.execute("""INSERT INTO Files(folder_id, file_name,
                       file_id, account_id, file_contents)
                       VALUES(?,?,?,?,?)""", self.current_folder, name, self.current_file, self.user_id, contents)
        connection.commit()
        self.get_all_files()

    def delete_file(self):
        """
        Delete the selected text file in the GUI from the database.

        This method attempts to delete the currently selected text file from the database and updates the GUI accordingly.

        """
        try:
            cursor.execute("""DELETE FROM Files
                        WHERE file_id = ? AND folder_id = ? AND account_id = ?""",
                        self.current_file,
                        self.current_folder,
                        self.user_id)
            connection.commit()
        except:
            print("No file selected")
        clear_window()
        Interface(root, self.screen_width, self.screen_height, self.username, self.user_id)

    def save_txt(self):
        """
        Save changes made to the currently opened text file.

        This method saves the edited content and name of the currently opened text file in the GUI.

        """
        name = self.my_entry1.get()
        contents = self.my_text1.get(0.0, END)
        cursor.execute("""UPDATE Files
                       SET file_contents = ?, file_name = ?
                       WHERE account_id = ? AND folder_id = ? AND file_id = ?"""
                       , contents, name, self.user_id, self.current_folder, self.current_file)
        connection.commit()
        self.get_all_files()

    def run_folder_creation(self):
        """
        Display the folder creation UI in the GUI.

        This method displays the user interface for creating a new folder.

        """
        self.directory_create_frame.place(x=400, y=300)

    def createFolder(self, cancel):
        """
        Create a new folder in the GUI and database.

        This method creates a new folder in the current directory or folder if the user chooses to proceed.

        Args:
            cancel (bool): If True, the folder creation is canceled; if False, a new folder is created.

        """
        self.directory_create_frame.place_forget()
        if cancel == False:
            name = self.folder_name_entry.get()
            found = False
            i = 0
            while found == False:
                if i not in self.folder_id_array:
                    found = True
                else:
                    i = i + 1
            self.folder_id = i
            cursor.execute("""INSERT INTO Folders(folder_id, folder_name,account_id,directory_in_id)
                        VALUES(?,?,?,?)""", self.folder_id, name, self.user_id, self.current_folder)
            connection.commit()
        clear_window()
        Interface(root, self.screen_width, self.screen_height, self.username, self.user_id)

    def update_textsize(self, text_size):
        """
        Update the text size of the text editor in the GUI.

        This method allows the user to change the text size of the text editor in the GUI.

        Args:
            text_size (int): The desired text size.
        """
        self.my_text1.configure(font=("Helvetica", text_size))


class Settings:
    def __init__(self, user_id, username):
        """
        Initialize the Settings class.

        Args:
            user_id (int): The user's account ID.
            username (str): The user's current username.
        """
        self.user_id = user_id
        self.username = username
        # Color theme arrays
        self.dark = ["#0D0D0D","#262626","#404040","#3A3B3A"]
        self.light = ["#737373","#D9D9D9","#F2F2F2","#2CA5DE"]
        self.blue = ["#225A76","#3FCEF6","#318EAD","#E33722"]
        self.red = ["#CC0100","#FF0100","#7F0100","#DE2C6E"]
        self.green = ["#6BBF90", "#B0D9C1", "#D9BCA3","#55E689"]
        self.purple = ["#4F3981","#654D97","#6C5A9F","#5E4890"]
        self.colour_array = ["dark", "light", "blue", "red", "green", "purple"]

        self.get_account()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the graphical user interface for the settings page.
        """
        self.frame = customtkinter.CTkFrame(root, fg_color=colour_theme1,
                                            height=700,
                                            width=1200)
        self.frame.place(x=250, y=250)

        self.sign_out_button = customtkinter.CTkButton(self.frame, text="Sign out!",
                                                       hover_color=colour_theme3,
                                                        fg_color=colour_theme1,
                                                        border_color=colour_theme2,
                                                        border_width=3,
                                                       command=self.sign_out)
        self.sign_out_button.pack(pady=15,padx=300)

        self.account_label = customtkinter.CTkLabel(self.frame,
                                                    text_color=colour_theme3,
                                                    text="Account:")
        self.account_label.pack()

        self.user_label = customtkinter.CTkLabel(self.frame,
                                                 text_color=colour_theme3,
                                                 text="Username:")
        self.user_label.pack()

        self.custom_name = customtkinter.CTkEntry(self.frame,
                                                fg_color=colour_theme2,
                                                border_color=colour_theme1,
                                                border_width=3,
                                                placeholder_text=self.username)
        self.custom_name.pack()

        self.save_name = customtkinter.CTkButton(self.frame, text="Save new username!",
                                                hover_color=colour_theme3,
                                                fg_color=colour_theme1,
                                                border_color=colour_theme2,
                                                border_width=3,
                                                command=partial(self.save_info, "user"))
        self.save_name.pack()

        self.email_label = customtkinter.CTkLabel(self.frame,
                                                  text_color=colour_theme3, text="Email:")
        self.email_label.pack()

        self.custom_email = customtkinter.CTkEntry(self.frame, fg_color=colour_theme2,
                                                border_color=colour_theme1,
                                                border_width=3,
                                                placeholder_text=self.account[1])
        self.custom_email.pack()

        self.save_email = customtkinter.CTkButton(self.frame, text="Save new email!",
                                                    hover_color=colour_theme3,
                                                    fg_color=colour_theme1,
                                                    border_color=colour_theme2,
                                                    border_width=3,
                                                    command=partial(self.save_info, "email"))
        self.save_email.pack()

        self.pass_label = customtkinter.CTkLabel(self.frame,
                                                 text_color=colour_theme3, text="New password:")
        self.pass_label.pack()

        self.custom_pass = customtkinter.CTkEntry(self.frame,
                                                fg_color=colour_theme2,
                                                border_color=colour_theme1,
                                                border_width=3,
                                                placeholder_text="New password")
        self.custom_pass.pack()

        self.save_pass = customtkinter.CTkButton(self.frame, text="Save new password!",
                                                hover_color=colour_theme3,
                                                fg_color=colour_theme1,
                                                border_color=colour_theme2,
                                                border_width=3,
                                                command=partial(self.save_info, "password"))
        self.save_pass.pack()

        self.diff_label = customtkinter.CTkLabel(self.frame,text_color=colour_theme3, text="Current exam difficulty:")
        self.diff_label.pack()

        self.diff_level = customtkinter.CTkLabel(self.frame,text_color=colour_theme3, text=round(self.account[3]))
        self.diff_level.pack()

        self.apperance = customtkinter.CTkLabel(self.frame,
                                                text_color=colour_theme3, text="Colour themes")
        self.apperance.pack()

        

        self.colour_choice = customtkinter.CTkComboBox(self.frame,fg_color=colour_theme2,
                                                        border_color=colour_theme1,
                                                        border_width=3,
                                                        button_color=colour_theme3)
        self.colour_choice.set("Select subject")
        self.colour_choice.configure(values=self.colour_array)
        self.colour_choice.pack()

        self.save_apperance = customtkinter.CTkButton(self.frame,
                                                    hover_color=colour_theme3,
                                                    fg_color=colour_theme1,
                                                    border_color=colour_theme2,
                                                    border_width=3,
                                                    text="Save colour!",command=self.save_colour)
        self.save_apperance.pack()

    def get_account(self):
        """
        Retrieve user account information from the database.
        """
        self.account = cursor.execute("""SELECT username, email, 
                                      password, user_difficulty
                                      FROM Accounts
                                      WHERE account_id = ?""",
                                      self.user_id).fetchone()
        self.all_user = cursor.execute("""SELECT username
                                       FROM Accounts
                                       Where account_id = ?""",
                                       self.user_id).fetchall()

    def save_colour(self):
        colour = self.colour_choice.get()
        array = None
        if colour == "dark":
            array = self.dark
        elif colour == "light":
            array = self.light
        elif colour == "blue":
            array = self.blue
        elif colour == "red":
            array = self.red
        elif colour == "green":
            array = self.green
        elif colour == "purple":
            array = self.purple

        if array is not None:
            root.configure(bg=array[3])  # Update the background color
        global colour_theme1
        global colour_theme2
        global colour_theme3
        colour_theme1 = array[0]
        colour_theme2 = array[1]
        colour_theme3 = array[2]

    def sign_out(self):
        """
        Sign the user out of their account.
        """
        file = open("Skip login.txt", "w")
        file.write("")
        clear_window()
        Login_System(root)

    def save_info(self, type):
        """
        Save user information changes (username, email, or password).

        Args:
            type (str): The type of information to save: "user", "email", or "password".
        """
        can_create = True
        if type == "user":
            input = self.custom_name.get()
            column = "username"
            for i in range(len(self.all_user)):
                if input == self.all_user[i]:
                    can_create = False
            if len(input) < 6:
                can_create = False
        if type == "email":
            input = self.custom_email.get()
            column = "email"
            if "@" not in input and len(input) < 8 and "." not in input:
                can_create = False
        if type == "password":
            input = self.custom_pass.get()
            column = "password"
            can_create = False
            if len(input) > 8:
                for char in input:
                    if char.isupper() == True:
                        for char in input:
                            if char.isnumeric() == True:
                                can_create = True
        if can_create == True:
            cursor.execute("""UPDATE Accounts
                        SET ? = ?
                        WHERE account_id = ?""", column, input, self.user_id)
            connection.commit()

        
class Login_System:
    def __init__(self, root):
        """
        Initialize the Login_System class.

        Args:
            root: The root window or main application window.
        """
        self.userid_array = []  # An array to store user IDs
        self.root = root
        self.user_id = 0
        self.dont_write = False
        self.access_granted = False
        self.can_create = False
        self.hidden_password = ""
        self.setup_ui(root)
        self.try_skip()

    def setup_ui(self, root):
        """
        Set up the graphical user interface for the login system.

        Args:
            root: The main application window.
        """
        self.entry_frame = Frame(root, background=colour_theme1)
        self.entry_frame.pack()

        self.title = customtkinter.CTkLabel(self.entry_frame,
                                            text_color=colour_theme3,
                                            text="Enter details")
        self.title.pack(anchor=NW, padx=20, pady=10)

        # Username input fields
        self.username_frame = customtkinter.CTkFrame(self.entry_frame,
                                                     fg_color=colour_theme1)
        self.username_frame.pack(padx=10, pady=5)

        self.label_username = customtkinter.CTkLabel(self.username_frame,
                                                     text_color=colour_theme3,
                                                     text="Username", font=("Helvetica", 12))
        self.label_username.pack(anchor=W, padx=5, pady=1)

        self.username_entry = customtkinter.CTkEntry(self.username_frame,
                                                     fg_color=colour_theme2,
                                                     border_color=colour_theme1,
                                                     border_width=3, width=400,
                                                     height=40, font=("Helvetica", 15))
        self.username_entry.pack()

        self.username_criteria = customtkinter.CTkLabel(self.username_frame,
                                                        text="Usernames must be at least 5 characters.",
                                                        text_color=colour_theme3)
        self.username_criteria.pack()

        # Email input fields
        self.email_frame = customtkinter.CTkFrame(self.entry_frame, fg_color=colour_theme1)
        self.email_frame.pack(padx=10, pady=5)

        self.label_email = customtkinter.CTkLabel(self.email_frame, text_color=colour_theme3,
                                                  text="Email", font=("Helvetica", 12))
        self.label_email.pack(anchor=W, padx=5, pady=1)

        self.email_entry = customtkinter.CTkEntry(self.email_frame, fg_color=colour_theme2,
                                                  border_color=colour_theme1, border_width=3,
                                                  width=400, height=40, font=("Helvetica", 15))
        self.email_entry.pack()

        self.email_criteria = customtkinter.CTkLabel(self.email_frame,
                                                     text="Your email must contain: an @, a dot, and be longer than 8 characters.",
                                                     text_color=colour_theme3)
        self.email_criteria.pack()

        # Password input fields
        self.password_frame = customtkinter.CTkFrame(self.entry_frame, fg_color=colour_theme1)
        self.password_frame.pack(padx=10, pady=5)

        self.label_password = customtkinter.CTkLabel(self.password_frame, text_color=colour_theme3,
                                                     text="Password", font=("Helvetica", 12))
        self.label_password.pack(anchor=W, padx=5, pady=1)

        self.password_entry = customtkinter.CTkEntry(self.password_frame, fg_color=colour_theme2,
                                                     border_color=colour_theme1, border_width=3,
                                                     width=400, height=40, font=("Helvetica", 15))
        self.password_entry.pack()

        self.password_criteria = customtkinter.CTkLabel(self.password_frame,
                                                        text="Your password must contain: more than 8 characters, a capital, and a number.",
                                                        text_color=colour_theme3)
        self.password_criteria.pack()

        self.retry_frame = customtkinter.CTkFrame(self.password_frame, fg_color=colour_theme1,
                                                  height=0, width=0)
        self.retry_frame.pack()

        self.enter_button = customtkinter.CTkButton(self.entry_frame, text_color=colour_theme3,
                                                    hover_color=colour_theme3, fg_color=colour_theme1,
                                                    border_color=colour_theme2, border_width=3,
                                                    text="Enter", command=self.validate)
        self.enter_button.pack(pady=5, padx=20, anchor=SE)

        self.create_button = customtkinter.CTkButton(self.entry_frame, text_color=colour_theme3,
                                                     hover_color=colour_theme3, fg_color=colour_theme1,
                                                     border_color=colour_theme2, border_width=3,
                                                     text="Create account", command=self.create_account)
        self.create_button.pack(pady=5, padx=20, anchor=SE)

        self.retry_username = customtkinter.CTkLabel(self.retry_frame, text_color=colour_theme3,
                                                     text="Incorrect username entered!",
                                                     font=("Helvetica", 12))

        self.retry_password = customtkinter.CTkLabel(self.retry_frame, text_color=colour_theme3,
                                                     text="Incorrect password entered!",
                                                     font=("Helvetica", 12))

        self.retry_email = customtkinter.CTkLabel(self.retry_frame, text_color=colour_theme3,
                                                  text="Incorrect email entered!",
                                                  font=("Helvetica", 12))

        # Bind the password entry field to a key release event
        self.password_entry.bind("<KeyRelease>", self.password_hiding)

    def password_hiding(self, key):
        """
        Mask the password input as asterisks for security.

        Args:
            key: A key release event triggering this function.
        """
        if key.keysym == "BackSpace":
            self.password_entry.delete(0, END)
            self.hidden_password = ""
        elif key.char.isalnum():
            self.hidden_password = self.hidden_password + key.keysym
            characters_in = len(self.password_entry.get())
            self.password_entry.delete(0, END)
            hidden_password = "*" * characters_in
            self.password_entry.insert(0, hidden_password)

    def fetch_user_info(self):
        """
        Fetch user information based on the provided username.

        Retrieves account_id, email, and password from the database using the entered username.
        Adjusts the appearance of input fields based on user input.
        """
        self.username = self.username_entry.get()
        if self.username != "":
            self.username_entry.configure(fg_color=colour_theme2)
            self.email_entry.configure(fg_color=colour_theme3)
            self.password_entry.configure(fg_color=colour_theme3)
            cursor = connection.cursor()
            self.information = cursor.execute("""SELECT account_id, email, password
                                            FROM Accounts
                                            WHERE username = ?""",
                                            self.username).fetchone()
        else:
            self.username_entry.configure(fg_color="red")

    def validate(self):
        """
        Validate the user's login details and use password hashing for secure comparison.

        This method checks if the entered username and email match the stored user information in the database.
        It retrieves the hashed password from the database and compares it with the hashed input password.
        If the username, email, and hashed password match, the user is granted access.

        The password is securely hashed using a combination of the input password and a salt before comparison.

        Raises:
            If any of the entered details (username, email) do not match or the password is incorrect,
            relevant error messages are displayed and the user's access is denied.

        If access is granted, the method calls the 'login_complete' function to proceed with the login process.
        """
        self.retry_frame.pack()
        self.fetch_user_info()
        if self.username != "":
            try:
                self.user_id = self.information[0]
                self.user_email = self.information[1]
                self.user_password = self.information[2]
                print(self.hidden_password)
                input_password = str(self.hidden_password)
                salt = "3kd"
                database_password = input_password + salt
                hashed_database_password = hashlib.md5(database_password.encode())
                new_input_password = hashed_database_password.hexdigest()
                print(new_input_password)
                self.retry_username.pack_forget()
                if self.email_entry.get() == self.user_email:
                    self.access_granted = True
                    self.retry_email.pack_forget()
                    if str(new_input_password) == str(self.user_password):
                        self.retry_password.pack_forget()
                        self.retry_frame.pack_forget()
                        print("Correct entry")
                        self.access_granted = True
                    else:
                        self.access_granted = False
                        self.retry_password.pack_forget()
                        self.retry_password.pack()
                        print("Password is Incorrect")
                        self.password_entry.configure(fg_color="red")
                else:
                    self.access_granted = False
                    self.retry_email.pack_forget()
                    self.retry_email.pack()
                    self.email_entry.configure(fg_color="red")
                    print("Email is incorrect")
            except:
                self.retry_username.pack_forget()
                self.retry_username.pack()
                print("Account does not exist")
        if self.access_granted:
            self.login_complete()
            

    def load_existing_accounts(self):
        """
        Load existing user accounts from the database.

        This method retrieves information about existing user accounts from the database, including their account IDs and usernames.
        It populates the 'userid_array' list with the account IDs and assigns a new unique user ID to the current user.

        Returns:
            The method sets 'self.user_id' to the newly assigned unique user ID.
        """
        self.information = cursor.execute("""SELECT account_id, username
                                            FROM Accounts""").fetchall()
        for rows in range(len(self.information)):
            self.userid_array.append(self.information[rows][0])
        found = False
        i = 0
        while found == False:
            if i not in self.userid_array:
                found = True
            else:
                i = i + 1
        self.user_id = i


    def create_account(self):
        """
        Create a new user account based on provided information.

        This method verifies the provided username, email, and password to ensure they meet certain criteria.
        If the provided information passes the checks, a new user account is created.

        """
        self.load_existing_accounts()
        char = 0
        ats = 0
        dots = 0
        upper = 0
        numbers = 0
        i = 0
        self.can_create = True

        # Check if the username exists or is too short
        for i in range(len(self.information)):
            if self.information[i][1] == self.username_entry.get():
                self.can_create = False

        if len(self.username_entry.get()) < 5:
            self.can_create = False

        if len(self.username_entry.get()) > 8:
            for characters in self.email_entry.get():
                if characters == "@":
                    ats = ats + 1
                if characters == ".":
                    if ats == 1:
                        dots = dots + 1
                else:
                    char = char + 1
            if ats == 1 and dots > 0 and char > 10:
                pass
            else:
                self.can_create = False
        else:
            self.can_create = False

        if len(self.hidden_password) > 8:
            for characters in self.hidden_password:
                if characters.isupper() == True:
                    upper = upper + 1
                if characters.isnumeric():
                    numbers = numbers + 1
            if numbers > 0 and upper > 0:
                pass
            else:
                self.can_create = False
        else:
            self.can_create = False

        if self.can_create == True:
            password = str(self.hidden_password)
            salt = "3kd"
            database_password = password + salt
            hashed_database_password = hashlib.md5(database_password.encode())
            hashed_database_password_simple = hashed_database_password.hexdigest()

            # Insert the new account and a default folder for the user
            cursor.execute("""INSERT INTO Accounts (username, password,
                        email, account_id, user_difficulty,questions_answered)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                        str(self.username_entry.get()), hashed_database_password_simple,
                        str(self.email_entry.get()), int(self.user_id), 3, 0)
            
            cursor.execute("""INSERT INTO Folders (account_id, folder_id, folder_name)
                        VALUES (?, ?, ?)""", self.user_id, 0, "User folders")
            connection.commit()

            print("Created")
            self.login_complete()

    def try_skip(self):
        """
        Attempt to skip the login process using saved login information.

        This method reads the saved login information from a file, retrieves user data from the database, and attempts
        to validate the saved login information to log the user in automatically.

        """
        file = open("Skip login.txt", "r")
        lines = file.read()

        # Retrieve user information from the database
        self.information = cursor.execute("""SELECT username, email, password, account_id
                                        FROM Accounts""").fetchall()

        place = lines.find("$?$")
        password = lines[place + 3:len(lines)]
        salt = "3kd"
        database_password = password + salt
        hashed_database_password = hashlib.md5(database_password.encode())
        hashed_database_password_simple = hashed_database_password.hexdigest()
        lines = lines[0:place] + hashed_database_password_simple

        for rows in range(len(self.information)):
            if lines == self.information[rows][0] + self.information[rows][1] + self.information[rows][2]:
                self.user_id = self.information[rows][3]
                self.username = self.information[rows][0]
                self.row_line = rows
                self.dont_write = True
                self.login_complete()

    def login_complete(self):
        """
        Complete the login process and, if allowed, save login details.

        This method is called when the login process is successfully completed. It can save the user's login details to a file
        for convenience in the future allowing them to "Skip" the login process.

        If 'self.dont_write' is not True, the method saves the username, email, and hashed password to a file named "Skip login.txt."

        """
        if self.dont_write != True:
            self.username = self.username_entry.get()
            file = open("Skip login.txt", "w")
            put_in = self.username + self.email_entry.get() + "$?$" + self.hidden_password
            file.write(str(put_in))
            file.close()
        Interface(self.root, width, height, self.username, self.user_id)


class FlashcardApp:
    def __init__(self, root, username, user_id):
        """
        Initialize the FlashcardApp.

        Parameters:
            root (Tk): The root window of the application.
            username (str): The username of the user.
            user_id (int): The user's unique identifier.

        Attributes:
            username (str): The username of the user.
            user_id (int): The user's unique identifier.
            root (Tk): The root window of the application.
            already_done (list): A list to keep track of cards that have already been reviewed.

            # Seperate attributes
            all_cards (str): A string to store all flashcards.
            cards_array (list): An array to store flashcards as individual cards.
            is_quote (bool): Indicates if the card contains a quote.
            front_card (str): The front of the flashcard.
            whole_card (str): The entire flashcard.
            front_card_text (str): Text on the front of the flashcard.
            back_card_text (str): Text on the back of the flashcard.

            # Whole flashcard attributes
            flashid_array (list): An array to store flashcard IDs.
            accuracy_score_array (list): An array to store accuracy scores for flashcards.
            times_recalled_array (list): An array to store the number of times each card was recalled.
            next_recall_array (list): An array to store the next recall times for flashcards.

            # Flashcard statistic attributes
            current_card (int): Index of the current flashcard.
            is_hashtag (bool): Indicates if the card contains a hashtag.
            hashtag_count (int): Count of hashtags on a card.

            # Attributes used throughout the methods

            difficulty (str): The difficulty level of the flashcard.
            accuracy_score_pattern (str or int): The pattern for accuracy scores.
            times_recalled_pattern (str or int): The pattern for the number of times a card was recalled.
            next_recall (str or int): The next recall time for a flashcard.
            improvements_required (bool): Indicates if improvements are required in recalling cards.

        Initializes the FlashcardApp, clears the window, loads flashcards, and sets up the user interface.
        """
        self.username = username
        self.user_id = user_id
        self.root = root
        self.already_done = []

        # Seperate attributes
        self.all_cards = ""
        self.cards_array = []
        self.is_quote = False
        self.front_card = ""
        self.whole_card = ""
        self.front_card_text = ""
        self.back_card_text = ""

        # Whole flashcard attributes
        self.flashid_array = []
        self.accuracy_score_array = []
        self.times_recalled_array = []
        self.next_recall_array = []

        # Attributes used throughout the methods
        self.current_card = 0
        self.is_hashtag = False
        self.hashtag_count = 0

        # Attributes identified and updating the card's statistics
        self.difficulty = ""
        self.accuracy_score_pattern = str or int
        self.times_recalled_pattern = str or int
        self.next_recall = str or int
        self.improvements_required = bool

        clear_window()
        self.load_flashcards()
        self.run_queue()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for the FlashcardApp.

        This method creates the frames, buttons, and labels for displaying flashcards and managing them.
        It includes sections for showing the front and back of the cards, offering options for recalling, and providing
        improvements for challenging cards or skipping them. It also handles completing all flashcards and exiting.

        """
        # Create a frame for the front of the flashcard.
        self.question_frame = customtkinter.CTkFrame(root, width=1100, fg_color=colour_theme1, height=600)
        self.question_frame.place(x=250, y=30)

        # Display the front of the flashcard.
        self.front_card_question = customtkinter.CTkLabel(self.question_frame, text=self.front(), font=("Helvetica", 33))
        self.front_card_question.place(x=50, y=50)

        # Create a button to show the answer.
        self.show_button = customtkinter.CTkButton(self.question_frame, hover_color=colour_theme3, fg_color=colour_theme1,
                                                border_color=colour_theme2, border_width=3, text="Show answer",
                                                width=1000, height=60, command=self.show_back)
        self.show_button.place(x=50, y=500)

        # Create a frame for the back of the flashcard.
        self.answer_frame = customtkinter.CTkFrame(root, fg_color=colour_theme1, height=600, width=1100)

        # Display the back of the flashcard.
        self.back_card_answer = customtkinter.CTkLabel(self.answer_frame, text=line_making(self.get_front() + " ➝ " + self.get_back(), 50),
                                                    font=("Helvetica", 33))
        self.back_card_answer.place(x=50, y=50)

        # Create buttons for managing flashcards.
        self.skip_button = customtkinter.CTkButton(self.answer_frame, hover_color=colour_theme3, fg_color=colour_theme1,
                                                border_color=colour_theme2, border_width=3, text="Skip",
                                                command=partial(self.card_running_system, "Skip"))
        self.skip_button.place(x=150, y=500)

        self.easy_button = customtkinter.CTkButton(self.answer_frame, text="Easy", hover_color=colour_theme3,
                                                fg_color=colour_theme1, border_color=colour_theme2, border_width=3,
                                                command=partial(self.card_running_system, "Easy"))
        self.easy_button.place(x=400, y=500)

        self.managed_button = customtkinter.CTkButton(self.answer_frame, text="Managed", hover_color=colour_theme3,
                                                    fg_color=colour_theme1, border_color=colour_theme2, border_width=3,
                                                    command=partial(self.card_running_system, "Managed"))
        self.managed_button.place(x=650, y=500)

        self.challenging_button = customtkinter.CTkButton(self.answer_frame, text="Challenge", hover_color=colour_theme3,
                                                        fg_color=colour_theme1, border_color=colour_theme2, border_width=3,
                                                        command=partial(self.card_running_system, "Challenge"))
        self.challenging_button.place(x=900, y=500)

        # Create a frame for improvements and suggestions.
        self.improvements_frame = customtkinter.CTkFrame(root, fg_color=colour_theme1, width=1100, height=600)

        # Display text with improvement suggestions.
        self.improvements_text = customtkinter.CTkLabel(self.improvements_frame, text="Maybe you should consider altering your flashcard to help it stick in your memory, as you seem to be having trouble recalling this card.")
        self.improvements_text.place(x=50, y=30)

        # Create a button to edit the flashcard.
        self.edit_card_button = customtkinter.CTkButton(self.improvements_frame, hover_color=colour_theme3, fg_color=colour_theme1,
                                                        border_color=colour_theme2, border_width=3, text="Edit flashcard")
        self.edit_card_button.place(x=50, y=400)

        # Create a button to pass on improvements and return to the front of the card.
        self.pass_improvements = customtkinter.CTkButton(self.improvements_frame, hover_color=colour_theme3,
                                                        fg_color=colour_theme1, border_color=colour_theme2, border_width=3,
                                                        text="Maybe later", command=self.show_front,
                                                        width=1000, height=60)
        self.pass_improvements.place(x=50, y=500)

        # Create a frame to display a message upon completing all flashcards.
        self.complete_frame = customtkinter.CTkFrame(root, fg_color=colour_theme1, width=1100, height=600)

        # Display a message for completing all flashcards and an exit button.
        self.improvements_text = customtkinter.CTkLabel(self.complete_frame, text="Good job, you have completed all of your flashcards. You can return to your notes and make more flashcards by pressing the X in the corner.")
        self.improvements_text.place(x=50, y=30)

        self.exit_button = customtkinter.CTkButton(root, text="X", hover_color=colour_theme3, fg_color=colour_theme1,
                                                border_color=colour_theme2, border_width=3, command=self.exit_cards,
                                                width=20, height=30)
        self.exit_button.place(x=1300, y=50)


    def no_questions(self):
        """
        Display a message when the user runs out of flashcards.

        This method creates a message to inform the user that they have no flashcards left and suggests going to the
        creation app to generate more flashcards.

        """
        # Create an exit button to close the message.
        self.exit_button = customtkinter.CTkButton(root, text="X", hover_color=colour_theme3, fg_color=colour_theme1,
                                                border_color=colour_theme2, border_width=3, command=self.exit_cards,
                                                corner_radius=1, width=20, height=30)
        self.exit_button.place(x=1000, y=10)

        # Display a message to inform the user.
        label = customtkinter.CTkLabel(root, text="You have no flashcards, go to the creation app to generate some!",
                                    text_color=colour_theme3)
        label.place(x=200, y=40)


    def exit_cards(self):
        """
        Exit the flashcard app and return to the HomeScreen.

        This method closes the flashcard app and returns to the HomeScreen of the application.

        """
        HomeScreen(self.user_id, self.username)

    def front(self):
        """
        Get the front side of the current flashcard for display.

        This method retrieves the text for the front side of the current flashcard and formats it for display.

        Returns:
            str: The formatted text to display as the front side of the flashcard.
        """
        text1 = self.get_front()
        text2 = line_making(text1, 60)
        text = text2 + " ➝ ?"
        return text

    def load_flashcards(self):
        """
        Load flashcards data from the database.

        This method retrieves flashcard data for the user from the database, populates various data structures, and prepares
        the flashcards for practice.

        """
        # Load flashcard data from the database.
        self.information = cursor.execute("""SELECT flashcard, flashcard_id, next_recall,
                                            times_recalled, accuracy_score
                                            FROM Flashcards
                                        WHERE account_id = ?""", self.user_id).fetchall()

        # Populate lists with flashcard data.
        for rows in range(len(self.information)):
            self.cards_array.append(self.information[rows][0])
            self.flashid_array.append(self.information[rows][1])
            self.accuracy_score_array.append(self.information[rows][4])
            self.times_recalled_array.append(self.information[rows][3])
            self.next_recall_array.append(self.information[rows][2])

        

    def get_front(self):
        """
        Retrieve the front side of the current flashcard.

        This method extracts the text for the front side of the current flashcard from the flashcard data stored in the
        `cards_array`.

        Returns:
            str: The text for the front side of the current flashcard.
        """
        try:
            self.is_quote = False
            self.is_hashtag = False
            self.front_card_text = ""
            self.whole_card = self.cards_array[self.current_card]
            for characters in self.whole_card:
                if characters == "#":
                    self.hashtag_count += 1
                    if self.hashtag_count == 2:
                        self.front_card_text += characters
                        self.front_card_text = self.front_card_text.replace("##", "")
                        self.is_hashtag = not self.is_hashtag
                        self.hashtag_count = 0
                if not self.is_hashtag:
                    self.front_card_text += characters
            return self.front_card_text
        except:
            self.no_questions()
            # Logic to get the front of the flashcard

    def get_back(self):
        """
        Retrieve the back side of the current flashcard.

        This method extracts the text for the back side of the current flashcard from the flashcard data stored in the
        `cards_array`.

        Returns:
            str: The text for the back side of the current flashcard.
        """
        self.is_quote = False
        self.is_hashtag = False
        self.back_card_text = ""
        self.whole_card = self.cards_array[self.current_card]
        for characters in self.whole_card:
            if self.is_hashtag:
                self.back_card_text += characters
                self.hashtag_count = 0
            if characters == "#":
                self.hashtag_count += 1
                if self.hashtag_count == 2:
                    self.is_hashtag = not self.is_hashtag
                    self.hashtag_count = 0
        return self.back_card_text

    
    def run_sort(self, array):
        """
        Perform quicksort on an array of items.

        Args:
            array (list): The input list to be sorted.

        Returns:
            list: The sorted list.

        Quick sort is a sorting algorithm that uses a divide-and-conquer approach to sort an array.
        The algorithm works as follows:
        - If the array has 1 or fewer elements, it is considered sorted and returned.
        - Choose a 'pivot' element from the array. The choice of the pivot can impact the algorithm's efficiency.
        - Partition the array into two sub-arrays: elements less than the pivot and elements greater than or equal to the pivot.
        - Recursively apply the quicksort algorithm to the sub-arrays.
        - Combine the sorted sub-arrays and the pivot to get the final sorted array.

        This implementation uses a recursive approach.

        Args:
            array (list): The input list to be sorted.

        Returns:
            list: The sorted list.

        Time Complexity:
        The average time complexity of quicksort is O(n log n), where n is the number of elements in the array.
        """
        # Base case: If the array has 1 or fewer elements, it's considered sorted and returned.
        if len(array) <= 1:
            return array

        # Initialize lists for elements greater and less than the pivot.
        final_array = []
        longest = []
        shortest = []

        # Choose the pivot element (here, the last element).
        pivot = array[-1]

        for i in range(len(array) - 1):
            # Compare the first element of each item in the array with the pivot.
            if array[i][0] > pivot[0]:
                longest.append(array[i])
            else:
                shortest.append(array[i])

        # Recursively apply quicksort to the sub-arrays if they are not empty.
        if len(longest) > 0:
            longest = self.run_sort(longest)
        if len(shortest) > 0:
            shortest = self.run_sort(shortest)

        # Combine the sorted sub-arrays and the pivot to get the final sorted array.
        final_array = longest + [pivot] + shortest
        return final_array


    def run_queue(self):
        """
        Initialize the queue with flashcards to be shown in a sorted order.

        The flashcards are sorted based on their 'next_recall' attribute, and the queue is prepared for presentation.
        """
        mixed_array = []
        for i in range(len(self.next_recall_array)):
            mixed_array.append([self.next_recall_array[i], self.flashid_array[i]])
        self.already_done = self.run_sort(mixed_array)
        self.already_done = deque(self.already_done)

    def chose_card(self):
        """
        Choose the next flashcard from the sorted queue.
        """
        self.current_card = self.already_done.popleft()
        self.current_card = self.current_card[1]

    def flashcards_complete(self):
        """
        Handle the situation when all flashcards have been presented.
        """
        self.answer_frame.place_forget()
        self.question_frame.place_forget()
        self.complete_frame.place(x=250, y=50)

    def card_running_system(self, button):
        """
        Handle the card running system, including updating card statistics and deciding the next action.

        Args:
            button (str): The button clicked, representing the user's assessment of the flashcard.

        This method performs several tasks:
        1. Chooses the next flashcard from the queue.
        2. Updates the flashcard's accuracy score, times recalled, and recall time based on the user's assessment.
        3. Calculates whether improvements are required.
        4. Updates the database with the new flashcard statistics.
        5. Decides whether to show the flashcard's front or display improvement suggestions.
        """
        if len(self.already_done) == 0:
            self.flashcards_complete()
        else:
            self.chose_card()
        self.difficulty = button
        self.accuracy_score = self.accuracy_score_array[self.current_card]
        self.times_recalled = self.times_recalled_array[self.current_card]
        self.next_recall = self.next_recall_array[self.current_card]

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
        self.update_database()
        if self.improvements_required:
            self.answer_frame.place_forget()
            self.improvements_frame.place(x=250, y=30)
            self.improvements_required = False
        else:
            self.show_front()

    def update_database(self):
        """
        Update the flashcard's statistics in the database.

        This method updates the flashcard's statistics in the database, including accuracy score, times recalled,
        and the next recall time. It uses the flashcard's unique identifier (flashcard_id) and the account_id
        to locate the specific flashcard for updating.

        The updated statistics are committed to the database.

        Parameters:
            - self.accuracy_score: The updated accuracy score of the flashcard.
            - self.times_recalled: The updated number of times the flashcard has been recalled.
            - self.next_recall: The updated next recall time for the flashcard.
        """
        cursor.execute("""UPDATE Flashcards
                    SET accuracy_score = ?, 
                    times_recalled = ?, 
                    next_recall = ?
                    WHERE flashcard_id = ? AND account_id = ?""",
                    self.accuracy_score,
                    self.times_recalled,
                    self.next_recall,
                    self.flashid_array[self.current_card],
                    self.user_id)
        cursor.commit()

    def memory_calculator(self):
        """
        Calculate the next recall time for a flashcard based on its statistics.

        This method calculates the next recall time based on the flashcard's times recalled and accuracy score.
        The next recall time helps determine when the flashcard should be presented again.

        If the flashcard has been recalled multiple times, the method adjusts the next recall time accordingly.
        If the flashcard's accuracy score is positive, it decreases the next recall time, promoting more frequent practice.
        If the accuracy score is negative, the method may suggest improvements and extend the next recall time.

        In cases where improvements are suggested:
        - For accuracy scores below -5, the next recall time is significantly increased.
        - The calculation is based on the accuracy score's absolute value.

        The adjusted next recall time is then used to update the flashcard's statistics.

        This method sets the 'next_recall' attribute based on the calculated next recall time.
        """
        self.next_recall = 0

        if self.times_recalled > 3:
            if self.accuracy_score < -4:
                self.improvements_required = True

        if self.times_recalled >= 3:
            if self.accuracy_score >= 4:
                self.accuracy_score = self.accuracy_score - 1
                self.next_recall = -round(self.accuracy_score + (self.accuracy_score * 0.5))

            # Assign next recall time based on accuracy score
            if self.accuracy_score == 3:
                self.next_recall = 0
            elif self.accuracy_score <= 2:
                self.next_recall = 1

            # Handle negative accuracy scores
            if self.accuracy_score <= 1:
                self.next_recall = 3

            if self.accuracy_score <= 0:
                self.next_recall = 5

            if self.accuracy_score <= -1:
                self.next_recall = 7

            if self.accuracy_score <= -4:
                self.improvements_required = True
                temp_accuracy = abs(self.accuracy_score)
                temp_accuracy = math.floor((temp_accuracy + 2) * 1.25)
                self.next_recall = temp_accuracy

        if self.times_recalled == 2:
            # Assign next recall time based on accuracy score
            if self.accuracy_score <= 2:
                self.next_recall = 0
            elif self.accuracy_score <= 1:
                self.next_recall = 1

            # Handle negative accuracy scores
            if self.accuracy_score <= 0:
                self.next_recall = 2

            if self.accuracy_score <= -1:
                self.next_recall = 3

            if self.accuracy_score <= -3:
                temp_accuracy = abs(self.accuracy_score)
                temp_accuracy = math.floor((temp_accuracy + 1) * 1.5)
                self.next_recall = temp_accuracy

        if self.times_recalled == 1:
            # Assign next recall time based on accuracy score
            if self.accuracy_score <= 1:
                self.next_recall = 0

            # Handle negative accuracy scores
            if self.accuracy_score <= -1:
                self.next_recall = 1

            if self.accuracy_score <= -2:
                self.next_recall = 2

    def show_back(self):
        """
        Switch to displaying the back of the flashcard.

        This method hides the question frame and the improvements frame (if displayed), and displays
        the answer frame to show the back of the flashcard with the corresponding text.

        The text displayed is a combination of the front and back of the flashcard.

        This method is called when the user presses the "Show answer" button.

        """
        self.question_frame.place_forget()
        self.improvements_frame.place_forget()
        self.answer_frame.place(x=250, y=30)
        self.back_card_answer.configure(
            text=line_making(
                self.get_front() + " ➝ " + self.get_back(), 50))
        # Show the back of the flashcard

    def show_front(self):
        """
        Switch to displaying the front of the flashcard.

        This method hides the answer frame and the improvements frame (if displayed), and displays
        the question frame to show the front of the flashcard with the corresponding text.

        This method is called when the user chooses to continue with the flashcard.

        """
        self.answer_frame.place_forget()
        self.improvements_frame.place_forget()
        self.question_frame.place(x=250, y=30)
        self.front_card_question.configure(text=self.front())


class Flashcard_System:
    def __init__(self, root, user_id, username):
        """
        Initialize the Flashcard_System class.

        Args:
            root: The root window for the user interface.
            user_id: The unique user identifier for the current user.
            username: The username of the current user.

        Attributes:
            username (str): The username of the current user.
            user_id (int): The unique user identifier for the current user.
            whole_card (str): The full text of the flashcard.
            cards_array (list): A list to store the text of all flashcards.
            accuracy_score_array (list): A list to store the accuracy scores of flashcards.
            times_recalled_array (list): A list to store the number of times each flashcard was recalled.
            next_recall_array (list): A list to store the next recall time for each flashcard.
            flashid_array (list): A list to store the unique identifiers of each flashcard.
            i (int): An integer to keep track of the current flashcard being edited.
            count (str): An event that keeps track of changes in the text field for flashcards.

        Methods:
            load_text(): Load the text from the flashcards.
            load_existing_cards(): Load the existing flashcards from the database.
            setup_ui(): Set up the user interface for the flashcard system.
            count_flashcards(event): Count the number of flashcards while editing text.

        Returns:
            None
        """
        self.username = username
        self.user_id = user_id
        
        self.whole_card = ""
        self.cards_array = []
        self.accuracy_score_array = []
        self.times_recalled_array = []
        self.next_recall_array = []
        self.flashid_array = []

        self.i = 0

        self.load_text()
        self.load_existing_cards()
        clear_window()
        self.setup_ui()
        
        self.count = self.my_text1.bind("<Key>", self.count_flashcards)

    
    def setup_ui(self):
        """
        Set up the user interface for the Flashcard System.

        This method creates various widgets and frames for the flashcard system user interface.

        """
        # Create the main frame for the flashcard system.
        self.create_frame = customtkinter.CTkFrame(root, fg_color=colour_theme1, width=1000, height=1080)
        self.create_frame.place(x=0, y=0)

        # Create a help button.
        self.how_to_button = customtkinter.CTkButton(self.create_frame, hover_color=colour_theme3, fg_color=colour_theme1, border_color=colour_theme2, border_width=3, width=30, height=30, text="?", command=self.how_to_create)
        self.how_to_button.place(x=600, y=30)

        # Create a frame for displaying flashcards.
        self.cards_frame = customtkinter.CTkFrame(root, fg_color=colour_theme1, width=500, height=500)
        self.cards_frame.place(x=1020, y=0)

        # Create a frame for providing user advice.
        self.advice_frame = customtkinter.CTkFrame(root, fg_color=colour_theme1, width=1000, height=1080)

        # Create a label for explaining the flashcard system.
        self.explain_label = customtkinter.CTkLabel(self.advice_frame, text=self.text1, text_color=colour_theme3, font=("Helvetica", 30))
        self.explain_label.pack(pady=6, padx=6)

        # Create instructions for using the flashcard system.
        self.instructions = customtkinter.CTkLabel(self.advice_frame, text=self.text_ins, text_color=colour_theme3, font=("Helvetica", 22))
        self.instructions.pack()

        # Create a button for creating flashcards.
        self.create_now = customtkinter.CTkButton(self.advice_frame, text="Create now!", hover_color=colour_theme3, fg_color=colour_theme1, border_color=colour_theme2, border_width=3, command=self.return_creating)
        self.create_now.pack(pady=5)

        # Create a label for indicating flashcard creation.
        self.label_create = customtkinter.CTkLabel(self.create_frame, text_color=colour_theme3, text="Create flashcards:", font=("Helvetica", 40))
        self.label_create.place(x=40, y=30)

        # Create a text box for entering flashcard content.
        self.my_text1 = customtkinter.CTkTextbox(self.create_frame, fg_color=colour_theme2, border_color=colour_theme1, border_width=3, width=900, height=500, font=("Helvetica", 40))
        self.my_text1.place(x=30, y=100)

        # Create a button to confirm flashcard creation.
        self.confirm_card = customtkinter.CTkButton(self.create_frame, hover_color=colour_theme3, fg_color=colour_theme1, border_color=colour_theme2, border_width=3, text="Confirm cards", command=self.create_flashcards)
        self.confirm_card.place(x=700, y=30)

        # Create a canvas for displaying flashcards.
        self.flashcards_canvas = customtkinter.CTkCanvas(self.cards_frame, background=colour_theme1, width=495, height=780)
        self.flashcards_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for scrolling through flashcards.
        self.flashcard_scrollbar = customtkinter.CTkScrollbar(self.cards_frame, command=self.flashcards_canvas.yview)
        self.flashcard_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a frame for flashcard content.
        self.flashcard_canvas_inner = customtkinter.CTkFrame(self.flashcards_canvas, fg_color=colour_theme1, width=500, height=900)
        self.flashcards_canvas.create_window((0, 0), window=self.flashcard_canvas_inner, anchor=NW)

        # Create a label for editing flashcards.
        self.edit_label = customtkinter.CTkLabel(self.flashcard_canvas_inner, text_color=colour_theme3, text="Click on flashcard to edit:", font=("Helvetica", 40))
        self.edit_label.pack(padx=15, pady=10)

        # Iterate through flashcards and create display frames.
        for cards in self.cards_array:
            flashcard = self.cards_array[self.i]
            flashcard = flashcard.replace("##", " ➝ ")
            end = False
            times_repeated = 0
            i = 0
            word_start = 0
            while end != True:
                i = i + 1
                try:
                    if flashcard[i] == " ":
                        word_start = i

                    if i == 50:
                        i = i + times_repeated * 50
                        flashcard = flashcard[:word_start] + "\n" + flashcard[word_start:]
                        times_repeated = times_repeated + 1
                except:
                    end = True

            if cards != "":
                frame = customtkinter.CTkFrame(self.flashcard_canvas_inner, border_color=colour_theme2, border_width=3, fg_color=colour_theme1, height=150, width=400)
                frame.pack(pady=5, padx=0)

                # Create a label to display the flashcard content.
                label_card = customtkinter.CTkLabel(frame, text_color=colour_theme3, text=flashcard, font=("Helvetica", 15))
                label_card.place(x=5, y=5)
                frame.bind("<Button-1>", partial(self.on_frame_click, self.i))

                # Create a button to delete flashcards.
                delete_card = customtkinter.CTkButton(frame, fg_color=colour_theme3, width=40, height=40, image=delete_image, text="", command=partial(self.remove_card, self.flashid_array[self.i]))
                delete_card.place(x=20, y=100)

            self.i = self.i + 1

        self.flashcard_canvas_inner.update_idletasks()
        self.flashcards_canvas.configure(scrollregion=self.flashcards_canvas.bbox("all"))
        self.flashcards_canvas.update_idletasks()
        self.flashcards_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.flashcards_canvas.configure(yscrollcommand=self.flashcard_scrollbar.set)

        # Create input fields for editing flashcards.
        self.front_label = customtkinter.CTkLabel(self.create_frame, text_color=colour_theme3, text="Edit front of card:", font=("Helvetica", 25))
        self.front_entry = customtkinter.CTkEntry(self.create_frame, fg_color=colour_theme2, border_color=colour_theme1, border_width=3, width=400, height=40, font=("Helvetica", 20))
        self.arrow_label = customtkinter.CTkLabel(self.create_frame, text_color=colour_theme3, text="➝", font=("Helvetica", 40))
        self.back_label = customtkinter.CTkLabel(self.create_frame, text_color=colour_theme3, text="Edit back of card:", font=("Helvetica", 25))
        self.back_entry = customtkinter.CTkEntry(self.create_frame, fg_color=colour_theme2, border_color=colour_theme1, border_width=3, width=400, height=40, font=("Helvetica", 20))

        # Create a button to confirm flashcard edits.
        self.confirm_edit = customtkinter.CTkButton(self.create_frame, hover_color=colour_theme3, fg_color=colour_theme1, border_color=colour_theme2, border_width=3, text="Save changes->", command=self.save_changes)

        # Create a button to exit the flashcard system.
        self.exit_button = customtkinter.CTkButton(root, text="X", hover_color=colour_theme3, fg_color=colour_theme1, border_color=colour_theme2, border_width=3, command=self.exit_cards, corner_radius=1, width=20, height=30)
        self.exit_button.place(x=1000, y=10)

    def exit_cards(self):
        """
        Exit the flashcard creation and return to the HomeScreen.
        """
        HomeScreen(self.user_id, self.username)

    def reset_window(self):
        """
        Reset the Flashcard_System window to its initial state.
        """
        self.__init__(root, self.user_id, self.username)

    def how_to_create(self):
        """
        Display instructions on how to create flashcards.
        """
        self.create_frame.place_forget()
        self.advice_frame.place(x=100, y=100)

    def return_creating(self):
        """
        Return to the flashcard creation interface.
        """
        self.create_frame.place(x=0, y=0)
        self.advice_frame.place_forget()

    def load_text(self):
        """
        Load text for displaying instructions on how to create flashcards.
        """
        self.text1 = "You can create flashcards of any length here, and it's simple!"
        self.text2 = "\n\nStep 1: To create a flashcard, first input what you would like the front of your card to be. Our example will be 'What is the color of grass?'"
        self.text3 = "\n\nStep 2: Then input a hashtag twice after your front of card '##'"
        self.text4 = "\n\nStep 3: Now type in the back of your card. For our card, it will be 'The color of grass is green'. Once the program detects a key input, an arrow '➝' will be displayed, and you will be able to add this completed card to your current deck of flashcards!"
        self.text5 = "\n\nIf you have completed the steps correctly, you should have text that looks like this \n \nWhat is the color of grass?➝\nThe color of grass is green\n\nYou can now press the 'confirm cards' button, and the card will be added."
        text1 = self.text2 + self.text3 + self.text4 + self.text5
        self.text_ins = line_making(text1, 50)

    def remove_card(self, card):
        """
        Remove a flashcard from the database and reset the window.

        Args:
            card (int): The flashcard ID to be removed.
        """
        cursor.execute("""DELETE FROM Flashcards
                       WHERE flashcard_id = ? AND account_id = ?""",
                       card,
                       self.user_id)
        connection.commit()
        self.reset_window()

    def on_frame_click(self, number, event):
        """
        Handle the click event on a flashcard frame, allowing for editing the selected flashcard.

        Args:
            number (int): The index of the selected flashcard.
            event: The click event triggered when the frame is clicked.
        """
        self.my_text1.place_forget()
        self.confirm_card.place_forget()
        self.front_label.place(x=150, y=200)
        self.front_entry.place(x=150, y=250)
        self.back_label.place(x=600, y=200)
        self.back_entry.place(x=600, y=250)
        self.confirm_edit.place(x=325, y=350)
        self.arrow_label.place(x=555, y=250)
        self.back_entry.delete(0, END)
        self.front_entry.delete(0, END)
        card = self.cards_array[number]
        middle = card.index("##")
        front = card[0:middle]
        back = card[middle + 2:len(card)]
        self.front_entry.insert(0, front)
        self.back_entry.insert(0, back)
        self.current_editting = self.flashid_array[number]

    def save_changes(self):
        """
        Save changes made to a flashcard, update the database, and reset the window.
        """
        self.new_card = self.front_entry.get() + "##" + self.back_entry.get()
        cursor.execute("""UPDATE Flashcards
                       SET flashcard = ?
                       WHERE flashcard_id = ? AND account_id = ?""",
                       self.new_card, self.current_editting, self.user_id)
        connection.commit()
        self.cards_frame.update_idletasks()
        self.__init__(root, self.user_id, self.username)

    def on_mousewheel(self, event):
        """
        Handle the mousewheel event for scrolling the flashcard canvas.

        Args:
            event: The mousewheel event.
        """
        self.flashcards_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def load_existing_cards(self):
        """
        Load existing flashcards from the database and initialize data structures.
        """
        self.information = cursor.execute("""SELECT flashcard, 
                                          flashcard_id, 
                                          next_recall,
                                          times_recalled, accuracy_score
                                          FROM Flashcards
                                          WHERE account_id = ?""",
                                          self.user_id).fetchall()
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
        """
        Create flashcards from the text input and save them to the database.
        """
        lines = 0
        for letter in self.my_text1.get(0.0, END):
            # if there is a new line, the lines count goes up by 1
            if letter == "\n":
                lines = lines + 1
            # if there is a "➝", it enters the card creation
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
                cursor.execute("""INSERT INTO Flashcards (account_id,
                               flashcard_id,flashcard,
                               accuracy_score,times_recalled,next_recall)
                            VALUES(?,?,?,0,0,0)""", self.user_id, i, str(front) + "##" + str(back))
                connection.commit()
                self.flashid_array.append(i)
        self.my_text1.delete(0.0, END)
        self.__init__(root, self.user_id, self.username)
    


    def front_card(self, lines):
        """
        Extract the front of the flashcard based on the line indicator.

        Args:
            lines (int): The line indicator where the flashcard front starts.

        Returns:
            str: The extracted front of the flashcard.
        """
        card_front = ""  # The list which will be returned as the front of the flashcard
        text_list = []  # The list containing all characters in the textbox
        line_count = 0  # The line counter to identify the line of the card
        i = 0  # The variable to traverse the text_list
        character = ""

        for letter in self.my_text1.get(0.0, END):
            text_list.append(letter)

        while character != "➝":
            i = i + 1
            if text_list[i - 1] == "\n":
                line_count = line_count + 1
            if line_count == lines:
                lines = lines + 1
                while character != "➝":
                    i = i + 1
                    if text_list[i - 2] == "\n":
                        character = "\n"
                    elif text_list[i - 2] == "➝":
                        character = "➝"
                    elif text_list[i - 2] == '"':
                        card_front.append("'")
                    else:
                        card_front = card_front + (text_list[i - 2])

        return card_front

    def back_card(self, lines):
        """
        Extract the back of the flashcard based on the line indicator.

        Args:
            lines (int): The line indicator where the flashcard back starts.

        Returns:
            str: The extracted back of the flashcard.
        """
        card_back = ""  # The list which will be returned as the back of the flashcard
        text_list = []  # The list containing all characters in the textbox
        i = 0  # The variable to traverse the text_list
        line_count = 0  # The line counter to identify the line of the card
        end_state = False  # A boolean variable to break the loop

        for letters in self.my_text1.get(0.0, END):
            text_list.append(letters)

        while end_state != True:
            i = i + 1
            if text_list[i] == "\n":
                line_count = line_count + 1
            if line_count == lines:
                i = i + 1
                while end_state != True:
                    i = i + 1
                    if text_list[i] == "➝":
                        i = i + 1
                        while end_state != True:
                            i = i + 1
                            if text_list[i] == "\n":
                                end_state = True
                            else:
                                card_back = card_back + text_list[i]

        return card_back
    
    def count_flashcards(self, value):
        """
        Count the number of hashtags in the textbox and create flashcards based on the hashtags.

        The method identifies pairs of consecutive hashtags ("##") and replaces them with a flashcard indicator "➝".

        """
        hashtag = 0  # The count of hashtags in the textbox

        for letters in self.my_text1.get(0.0, END):
            if letters == "#":
                hashtag = hashtag + 1  # Increment the hashtag counter

                if hashtag == 2:  # Check for the 2nd hashtag in a row
                    print("Flashcard created")
                    hashtag = 0  # Reset the hashtag counter

                    text_inside = self.my_text1.get(0.0, END)
                    text_inside = text_inside.replace("##", "➝")  # Replace "##" with the flashcard indicator "➝"
                    self.my_text1.delete(0.0, END)
                    self.my_text1.insert(END, text_inside)

            else:
                hashtag = 0  # Reset the hashtag counter


class AddQuestions:
    def __init__(self, user_id, username):
        """
        Initializes the AddQuestions class, setting up the user and UI elements.

        Args:
            user_id (int): The user's unique identifier.
            username (str): The username of the user.
        """
        self.user_id = user_id
        self.username = username
        self.subjects_array = ["Mathematics", "English", "Science", "Spanish", "Psychology", "Computer Science"]
        self.difficulty_array = ["Easy", "Moderate", "Intermediate", "Medium", "Difficult", "Challenge", "Expert", "Impossible"]
        clear_window()
        self.setup_ui()
        self.add_items()
        
    def setup_ui(self):
        """
        Sets up the user interface elements for question creation.
        """
        self.exit_button = customtkinter.CTkButton(root, text="X",
                                                   hover_color=colour_theme3,
                                                   fg_color=colour_theme1,
                                                   border_color=colour_theme2,
                                                   border_width=3, command=self.run_home,
                                                   width=20, height=30)
        self.exit_button.pack()

        # Labels and entry fields for inputting question, answer, education level, subject, and difficulty
        self.q_label = customtkinter.CTkLabel(root, text="Input question")
        self.q_label.pack()
        self.question = customtkinter.CTkEntry(root)
        self.question.pack()
        self.a_label = customtkinter.CTkLabel(root, text="Input answer")
        self.a_label.pack()
        self.answer = customtkinter.CTkEntry(root)
        self.answer.pack()
        self.ed_type_label = customtkinter.CTkLabel(root,
                                        text="Input type of education (e.g. GCSE, A-level)")
        self.ed_type_label.pack()
        self.ed_level = customtkinter.CTkEntry(root)
        self.ed_level.pack()
        self.sub_label = customtkinter.CTkLabel(root, text="Input subject")
        self.sub_label.pack()
        self.subject = customtkinter.CTkComboBox(root)
        self.subject.pack()
        self.dif_label = customtkinter.CTkLabel(root, text="Select difficulty")
        self.dif_label.pack()
        self.difficulty = customtkinter.CTkComboBox(root)
        self.difficulty.pack()

        # Button to save the question
        self.save = customtkinter.CTkButton(root, text="Save question", command=self.save_question)
        self.save.pack(pady=5)

    def run_home(self):
        """
        Navigates back to the home screen when the 'X' button is pressed.
        """
        clear_window()
        HomeScreen(self.user_id, self.username)

    def add_items(self):
        """
        Populates the subject and difficulty ComboBox with available options.
        """
        self.subject.set("Select subject")
        self.subject.configure(values=self.subjects_array)
        self.difficulty.set("Select difficulty")
        self.difficulty.configure(values=self.difficulty_array)

    def save_question(self):
        """
        Saves the entered question, answer, education level, subject, and difficulty to the database.
        """
        self.information = cursor.execute("""SELECT *
                                          FROM Questions
                                          INNER JOIN Subjects 
                                          ON Questions.subject_id = Subjects.subject_id
                                          INNER JOIN DifficultyLevels 
                                          ON Questions.difficulty_id = DifficultyLevels.difficulty_id
                                          """).fetchall()

        in_question = self.question.get()
        in_answer = self.answer.get()
        in_subject = self.subject.get()
        in_education_level = self.ed_level.get()
        in_difficulty = self.difficulty.get()
        question_id = len(self.information)

        in_subject = self.subjects_array.index(in_subject)
        in_difficulty = self.difficulty_array.index(in_difficulty)

        # Insert the question into the database
        cursor.execute("""INSERT INTO Questions (question_id,
                       subject_id, difficulty_id,
                       question, answer, education_type)
                       VALUES (?,?,?,?,?,?)""", question_id,
                       in_subject, in_difficulty, in_question,
                       in_answer, in_education_level)
        connection.commit()
        self.__init__()  # Reinitialize the class to clear input fields


class ExamQuestion:
    def __init__(self, user_id, username):
        """
        Initialize the ExamQuestion class.

        Args:
            user_id (int): The user's ID.
            username (str): The user's username.

        This method sets up the initial state of the ExamQuestion class, including user information and GUI elements.

        """
        self.user_id = user_id
        self.username = username
        self.subjects_array = ["Mathematics", "Spanish"]
        self.criteria_array = []
        self.given_answer_array = []
        self.answer_format = ""
        self.given_answer = ""
        self.score = int 

        clear_window()
        self.load_text()
        self.start_screen()
        self.add_items()

    def start_screen(self):
        """
        Display the initial screen for the ExamQuestion class.

        This method creates and displays the initial GUI components, including subject selection, question display, and answer input.

        """
        
        self.frame = customtkinter.CTkFrame(root,
                                            fg_color=colour_theme1,
                                            width=1200,height=900)
        self.frame.place(x=200,y=0)

        self.exit_button = customtkinter.CTkButton(root,text="X",
                                                   hover_color=colour_theme3,
                                                   fg_color=colour_theme1,
                                                   border_color=colour_theme2,
                                                   border_width=3,command=self.run_home, 
                                                   width=20,height=30)
        self.exit_button.place(x=1300,y=10)

        self.how_to_button = customtkinter.CTkButton(self.frame,hover_color=colour_theme3,
                                                     fg_color=colour_theme1,
                                                     border_color=colour_theme2,
                                                     border_width=3,width=30,
                                                     height=30, text="?",
                                                     command=self.how_to_create)
        self.how_to_button.place(x=10,y=10)

        self.add_button = customtkinter.CTkButton(self.frame,text="Create questions!",
                                                   hover_color=colour_theme3,
                                                   fg_color=colour_theme1,
                                                   border_color=colour_theme2,
                                                   border_width=3,command=self.create_questions)
        self.add_button.place(x=20,y=300)
        

        self.selection_frame = customtkinter.CTkFrame(root,width=1000,height=450)
        self.selection_frame.pack()
 
        self.advice_frame = customtkinter.CTkFrame(root,fg_color=colour_theme1,
                                                   width=1000, height=1080)

        self.explain_label = customtkinter.CTkLabel(self.advice_frame,text=self.text1,
                                                    text_color=colour_theme3, font=(
                                                        "Helvetica", 30))
        self.explain_label.pack(pady=6,padx=6)

        self.instructions = customtkinter.CTkLabel(self.advice_frame,text=self.text_ins,
                                                   text_color=colour_theme3, font=(
                                                       "Helvetica", 22))
        self.instructions.pack()

        self.create_now = customtkinter.CTkButton(self.advice_frame,text="Practice now!",
                                                  hover_color=colour_theme3,
                                                  fg_color=colour_theme1,
                                                  border_color=colour_theme2,
                                                  border_width=3,
                                                  command=self.return_creating)
        self.create_now.pack(pady=5)

        self.sub_label = customtkinter.CTkLabel(self.selection_frame,
                                                text="Input subject")
        self.sub_label.pack()

        self.subject = customtkinter.CTkComboBox(self.selection_frame)
        self.subject.pack()

        self.select_button = customtkinter.CTkButton(self.selection_frame,
                                                     hover_color=colour_theme3,
                                                     fg_color=colour_theme1,
                                                     border_color=colour_theme2,
                                                     border_width=3,text="Practice this!",
                                                     command=self.display_question)
        self.select_button.pack()

        self.question_area = customtkinter.CTkFrame(root,
                                                    bg_color=colour_theme2,
                                                    fg_color=colour_theme1,
                                                    border_color=colour_theme2,
                                                    border_width=3, width=1000, 
                                                    height=450)

        self.question = customtkinter.CTkLabel(self.question_area,
                                               text_color=colour_theme3,
                                               font=("Helvetica", 40),width=700)
        self.question.pack(pady=20)
 
        self.answer_area = customtkinter.CTkFrame(root,bg_color=colour_theme2,
                                                  fg_color=colour_theme1,
                                                  border_color=colour_theme2,
                                                  border_width=3,width=1100)

        self.answer_advice = customtkinter.CTkLabel(self.answer_area,
                                                    text_color=colour_theme3,
                                                    text="Do not include the format your answer should be in e.g. X =. The format should be provided already."
                                                    )
        self.answer_advice.place(x=10,y=10)

        self.format = customtkinter.CTkLabel(self.answer_area,text_color=colour_theme3)
        self.format.place(x=10,y=40)

        self.answer_input = customtkinter.CTkEntry(self.answer_area,text_color=colour_theme3,
                                                   fg_color=colour_theme1,
                                                   border_color=colour_theme2,border_width=3, 
                                                   font=("Helvetica", 20),width=1000)
        self.answer_input.place(x=70,y=40)
 
        self.enter_button = customtkinter.CTkButton(self.answer_area,text="Enter!",
                                                    width=70, height=70,hover_color=colour_theme3,
                                                    fg_color=colour_theme1,border_color=colour_theme2,
                                                    border_width=3, command=self.check_question)
        self.enter_button.place(x=1000,y=100)

        self.results_frame = customtkinter.CTkFrame(root,bg_color=colour_theme2,fg_color=colour_theme1,
                                                    border_color=colour_theme2,border_width=3)

        self.question_display = customtkinter.CTkLabel(self.results_frame,text_color=colour_theme3)
        self.question_display.pack()

        self.answer_display = customtkinter.CTkLabel(self.results_frame,text_color=colour_theme3)
        self.answer_display.pack(pady=0)
    
        self.given_display = customtkinter.CTkLabel(self.results_frame,text_color=colour_theme3)
        self.given_display.pack(pady=30)

        self.correct_indicator = customtkinter.CTkLabel(self.results_frame,text_color=colour_theme3)
        self.correct_indicator.pack(pady=15)

        self.next_question_button = customtkinter.CTkButton(self.results_frame,hover_color=colour_theme3,
                                                            fg_color=colour_theme1,
                                                            border_color=colour_theme2,
                                                            border_width=3,text="Next question",
                                                            command=self.display_question)
        self.next_question_button.pack(pady=4)

    def add_items(self):
        """
        Add items to the subject dropdown.

        This method sets the subject dropdown to display available subjects and selects "Select subject" by default.

        Returns:
            None
        """
        self.subject.set("Select subject")
        self.subject.configure(values=self.subjects_array)

    def create_questions(self):
        """
        Navigate to the question creation screen.

        This method clears the current window and opens the question creation screen.

        Returns:
            None
        """
        clear_window()
        AddQuestions(self.user_id, self.username)

    def run_home(self):
        """
        Return to the home screen.

        This method navigates the user back to the home screen.

        Returns:
            None
        """
        HomeScreen(self.user_id, self.username)

    def how_to_create(self):
        """
        Display guidance on how to create questions.

        This method displays guidance on creating questions for the user.

        Returns:
            None
        """
        self.advice_frame.pack(pady=10)

    def return_creating(self):
        """
        Hide the guidance on creating questions.

        This method hides the guidance on creating questions for the user.

        Returns:
            None
        """
        self.advice_frame.pack_forget()

    def load_text(self):
        """
        Load text information for guidance.

        This method loads text information to guide the user on how to use the application.

        Returns:
            None
        """
        self.text1 = "Practice exam questions and create your own for others to try!"
        text = "Step 1: To practice exam questions first select a subject\n\nStep 2: The question will be displayed and you will then be able to type your answer.\n\nStep 3: The results will be displayed, and depending on your performance, accuracy, question answered, and previous difficulty, you will be assigned a difficulty for your next question.\n\nStep 4: Now you may repeat these steps.\n\nIf you wish to create exam questions because you find yourself repeating the same questions, you may add to the database of questions yourself. However, we ask you to make them as accurate as possible for all user enjoyment!"
        text = line_making(text, 50)
        self.text_ins = text

    def check_question(self):
        # Initialize variables
        current_word = ""
        self.criteria_array = []
        self.given_answer_array = []

        # Loop through each character in the current answer
        for characters in self.current_answer:
            if characters == " ":
                # Check if the current word is an equals sign
                if current_word == "=":
                    self.answer_format = self.criteria_array[len(self.criteria_array) - 1] + " ="
                else:
                    self.criteria_array.append(current_word)
                current_word = ""
            else:
                if characters != "\n":
                    current_word = current_word + characters

        # Check and append the last word in the answer
        if current_word != "":
            if " " not in current_word:
                if "\n" not in current_word:
                    self.criteria_array.append(current_word)

        # Reset the current_word variable
        current_word = ""

        # Get the given answer from the input field
        self.given_answer = self.answer_input.get()

        # Loop through each character in the given answer
        for characters in self.given_answer:
            if characters == " ":
                self.given_answer_array.append(current_word)
                current_word = ""
            else:
                current_word = current_word + str(characters)

        # Check and append the last word in the given answer
        if current_word != "":
            if " " not in current_word:
                self.given_answer_array.append(current_word)

        # Initialize score and compare given answer with criteria
        self.score = 0
        for i in range(len(self.given_answer_array)):
            for j in range(len(self.criteria_array)):
                if self.given_answer_array[i] == self.criteria_array[j]:
                    self.score += 1

        try:
            # Calculate the percentage of correctness
            self.percent = 100 * (len(self.criteria_array) / self.score)
        except ZeroDivisionError:
            # Handle division by zero error
            self.percent = 0

        # Call the method to display results
        self.display_results()

    def display_results(self):
        """
        Displays the results of a question, including the question, answer, user's answer, and correctness indicator.
        Calculates the difficulty of the next question and updates the user's statistics.
        """
        self.question_area.pack_forget()
        self.answer_area.place_forget()
        self.question_display.configure(text="This is the question: " + self.current_question)
        self.answer_display.configure(text="This is the answer: " + self.current_answer)
        self.given_display.configure(text="This is your answer: " + self.given_answer)
        if self.percent > 70.0:
            self.correct_indicator.configure(text="Correct answer!")
        else:
            self.correct_indicator.configure(text="You got this question wrong!")
        self.results_frame.pack()
        self.difficulty_calculator()
        self.update_stats()

    def get_user_stats(self):
        """
        Retrieves the user's statistics, including user difficulty and the number of questions answered.
        """
        self.user_stats = cursor.execute("""SELECT user_difficulty, questions_answered
                                        FROM Accounts
                                        WHERE account_id = ?""", self.user_id).fetchone()
        print(self.user_stats)
        self.real_difficulty = self.user_stats[0]
        self.difficulty = round(self.real_difficulty, 0)
        self.questions_answered = self.user_stats[1]

    def update_stats(self):
        """
        Updates the user's statistics, including the user's new difficulty and the number of questions answered.
        """
        self.questions_answered = self.questions_answered + 1
        cursor.execute("""UPDATE Accounts
                    SET user_difficulty = ?, questions_answered = ?
                    WHERE account_id = ?""", self.new_difficulty,
                    self.questions_answered, self.user_id)
        cursor.commit()

    def choose_question(self, subject):
        """
        Chooses a question from the database based on the subject and user's difficulty level.
        """
        self.whole_question = cursor.execute("""SELECT question, answer, 
                                            question_id, answer_format
                                        FROM Questions
                                        INNER JOIN Subjects 
                                            ON Questions.subject_id = Subjects.subject_id
                                        WHERE difficulty_id = ? AND subject_name = ?
                                        """, self.difficulty, subject).fetchone()
        print(self.whole_question)
        self.current_question = self.whole_question[0]
        self.current_answer = self.whole_question[1]
        self.current_id = self.whole_question[2]
        self.question_format = self.whole_question[3]

    def display_question(self):
        """
        Displays a new question for the user to answer.
        Retrieves the user's statistics, chooses a question, and updates the interface.
        """
        self.results_frame.pack_forget()
        self.get_user_stats()
        self.answer_input.delete(0, END)
        in_subject = self.subject.get()
        self.selection_frame.pack_forget()
        self.choose_question(in_subject)
        self.question_area.pack(pady=50)
        self.question.pack(padx=5, pady=10)
        self.question.configure(text=self.current_question)
        if self.question_format == None:
            self.format.configure(text="")
        else:
            self.format.configure(text=self.question_format)
        self.answer_area.place(x=250, y=300)

    def difficulty_calculator(self):
        """
        Calculates the new difficulty level for the next question, incorporating a variety of factors
        to make the difficulty adapt to user performance in a dynamic and engaging way.

        Factors considered:
        1. Percentage of Correctness: If the user's performance falls below 70%, the difficulty decreases, 
        allowing for a smoother learning curve.
        2. Length of Criteria Array: If the user needs to remember fewer criteria, it's more forgiving
        if they get it wrong.
        3. Number of Questions Answered: Over time, the difficulty increases at a slower rate, providing
        a more challenging experience as the user progresses.
        4. Current User Difficulty: Taking into account the user's previous difficulty level to avoid 
        extreme fluctuations.

        The resulting difficulty level ensures the user receives questions appropriate to their skill level.
        """
        increase = 2.0  # Initialize the difficulty change factor

        # Adjust difficulty based on correctness percentage
        if self.percent < 70:
            increase = -(increase)  # Decrease difficulty if the user's performance is below 70%
            if len(self.criteria_array) < 3:
                try:
                    increase = increase * (1 - (self.percent / 100))  # Adjust difficulty based on correctness
                except:
                    increase = increase * 0.8  # Default decrease if unable to calculate based on percentage

        # Adjust difficulty based on the number of questions answered
        if self.questions_answered == 0:
            increase = increase / 0.9  # Adjust difficulty for the first question
        else:
            increase = increase / ((math.log(self.questions_answered)) + 0.7)  # Slower difficulty increase over time

        # Calculate the new difficulty level
        self.new_difficulty = self.real_difficulty + increase

        # Ensure difficulty remains within a reasonable range
        if self.new_difficulty > 7:
            self.new_difficulty = 7  # Upper limit for difficulty
        if self.new_difficulty < 0:
            self.new_difficulty = 0  # Lower limit for difficulty

        # The resulting difficulty change is determined by four variables, allowing the difficulty to adapt
        # dynamically to user performance, ensuring a balanced and engaging learning experience.


login_system1 = Login_System(root)
root.mainloop()
#this is how the window loops itself

#Change sql query format (Stops sql injection and looks cool)
#