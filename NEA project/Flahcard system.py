from tkinter import *
from tkinter import filedialog
import os, glob
from tkinter import messagebox
import customtkinter
os.chdir("./File folder/flashcard folder/")
root = Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue") 

root.title("Application")
root.geometry("1920x1080")
root.state("zoomed")
root.config()

class flashcard_system:
    def __init__ (self,root):

        self.text_box = customtkinter.CTkTextbox(root, width=1000, height=700)
        self.text_box.pack()

        self.button_get = customtkinter.CTkButton(root,text="Get", command=self.load_flashcards)
        self.button_get.pack()
        self.count = self.text_box.bind("<Key>", self.count_flashcards)
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
        for letter in self.text_box.get(0.0,END):
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
        for letters in self.text_box.get(0.0,END):
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
        for letter in self.text_box.get(0.0,END):
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
        for letters in self.text_box.get(0.0,END):
            #the if statement identifies the 1st instance of the "#"
            if letters == "#":
                hashtag = hashtag + 1
                #the next if statement identifies the 2nd hashtage as 2 in a row will result in the hashtag counter to = 2
                if hashtag == 2:
                    print("Flashcard created")
                    #to make sure the statement doesn't continuously repeat the variable is reset to 0
                    hashtag = 0
                    #this part replaces the "##" with the identifier of the flashcard
                    text_inside = self.text_box.get(0.0,END)
                    text_inside = text_inside.replace("##","➝")
                    self.text_box.delete(0.0,END)
                    self.text_box.insert(END,text_inside)
            #this else ensures that if there is not a repeat of the "#" after a 1st input that the hashtag value is reset
            else:
                hashtag=0

flashcard_system1 = flashcard_system(root)
root.mainloop()