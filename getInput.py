#!/usr/bin/python

from tkinter import *
from tkinter import font
import tkinter as tk
from tkinter.filedialog import askopenfile

source = "No file selected"

def choose_file(label):
    ### call global variables
    global source
    ### get file from user and update source label
    source = askopenfile(mode='r', filetypes=[('tab separated files', '*.tsv')])
#    print(source)
    label.config(text=source.name)


### Main calls start. The app starts here
def start():
    ### call global variables
    #    global source

    ### set constants
    background = "white"
    button_background = "#eee"

    ### build GUI
    root = Tk()
    root.geometry("440x620")
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=11)


    root["bg"] = background

    intro_frame = Frame(root, bd=7, bg=background)
    intro_frame.grid(row=1, column=1)
    intro_label = Label(intro_frame, bg=background, width=60, anchor="w",
                    text="Choose tab separated file listing protein binding")
    intro_label.grid(row=1, column=1)
    intro_label["anchor"] = "center"

    selected_frame = Frame(root, bd=7, bg=background)
    selected_frame.grid(row=3, column=1)
    selected_label = Label(selected_frame, bg=background, text=source)
    selected_label.grid(row=3, column=2)

    ### Select file here. Use lambda to pass label for updating as argument
    src_frame = Frame(root, bd=7, bg=background)
    src_frame.grid(row=2, column=1)
    src_file_button = Button(src_frame, bg=button_background, text='CHOOSE FILE', command=lambda:choose_file(selected_label))
    src_file_button.grid(row=2, column=4)

    root.mainloop()


if __name__ == "__main__":
    start()
