#!/usr/bin/python

from tkinter import *
from tkinter import font
import tkinter as tk
from tkinter.filedialog import askopenfile
import sys
import os.path
from os import path

source_name = "No file selected"
required_columns = list(("type1Name", "type2Name", "mutant"
                       , "oligo", "MT initiation Tm"))


def choose_file(label):
    ### call global variables
    global source_name
    ### get file from user and update source label
    source = askopenfile(mode='r', filetypes=[('tab separated files', '*.tsv')])
    source_name = source.name
#    print(source_name)
    label.config(text=source.name)


def count_binding(label):
    ### call global variables
    global source_name

    if source_name is not None:
        if source_name is not "No file selected":
            print(source_name)
            print(type(source_name))
            if path.isfile(source_name):
                read_file()
            else:
                label.config(text="File not found. Try again?")


def read_file():
    ### call global variables
    global source_name

    infile = open(source_name, "r")
    metadata = infile.readline()

    analysis_columns = {}
    data_results = {}
    analysis_columns = check_metadata(metadata)
    data = list()

    if len(analysis_columns) > 0:
        line_counter = 1
        for line in infile:
            if line_counter > 1:
#                print(line)
                analyze_line(line)

            line_counter += 1

#    content = infile.read()
#    print(type(content))
#    infile.close()


def check_metadata(metaline):
    global required_columns
    empty_loc = {}
    col_loc = {}

    for name in required_columns:
        if name not in metaline:
            return(empty_loc)
        else:
            col_loc[name] = metaline.index(name)

    return(col_loc)


def analyze_line(dataline):
    data = dataline.split("\t")


### Main calls start. The app starts here
def start():
    ### call global variables
#    global source_name

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
    intro_frame.pack()
    intro_label = Label(intro_frame, bg=background, width=60, anchor="w",
                    text="Choose tab separated file listing protein binding")
    intro_label.pack()
    intro_label["anchor"] = "center"

    selected_frame = Frame(root, bd=7, bg=background)
    selected_frame.pack()
    selected_label = Label(selected_frame, bg=background, text=source_name)
    selected_label.grid(row=3, column=2)

    ### Select file here. Use lambda to pass label for updating as argument
    src_frame = Frame(root, bd=7, bg=background)
    src_frame.pack()
    src_file_button = Button(src_frame, bg=button_background, text='CHOOSE FILE', command=lambda:choose_file(selected_label))
    src_file_button.pack(side="top", pady=10)

    start_btn = Button(src_frame, text='Run Analysis', command=lambda:count_binding(selected_label))
    start_btn.pack(side="left", padx=10, pady=10)
    close_btn = Button(src_frame, bg=button_background, text='Exit', command=lambda: sys.exit())
    close_btn.pack(side="right", padx=10, pady=10)



    root.mainloop()


if __name__ == "__main__":
    start()
