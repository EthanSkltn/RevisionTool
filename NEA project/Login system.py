from tkinter import *
from tkinter import filedialog
import os, glob
import customtkinter


root = Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue") 

root.title("Application")

root.config()

class Login_System:
    def __init__(self, root):
        self.access_granted = False
        self.setup_ui(root)

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

    def validate(self):
        user_failed = 0
        pass_failed = 0
        self.retry_frame.pack()
        try:
            filename = self.username_entry.get() + " Login details"
            file = open(filename, "r")
            line = file.readlines()[0:2]
            self.retry_username.pack_forget()
            if self.email_entry.get() + "\n" == line[0]:
                self.retry_email.pack_forget()
                if self.password_entry.get() == line[1]:
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
            file.close()
        except:
            if user_failed == 0:
                self.retry_username.pack_forget()
                self.retry_username.pack(anchor="w",pady=2)
                print("Account does not exist")
            user_failed = user_failed + 1
        self.login_complete()

    def create_account(self):
        try:
            char = 0
            ats = 0
            dots = 0
            upper = 0
            numbers = 0
            filename = self.username_entry.get() + " Login details"
            file = open(filename, "w")
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
                    if len(self.password_entry.get()) > 8:
                        for characters in self.password_entry.get():
                            if characters.isupper() == True:
                                upper = upper + 1
                            if characters.isnumeric():
                                numbers = numbers + 1
                        if numbers > 0 and upper > 0:
                            access_granted = True
                            file.write(self.email_entry.get())
                            file.write("\n" + self.password_entry.get())
        except:
            customtkinter.CTkLabel()
        self.login_complete()

    def login_complete(self):
        Login_System(self.root, width, height)
 
login_system1 = Login_System(root)
root.mainloop()
#this is how the window loops itself