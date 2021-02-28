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
type1_init_max = {}
mutant_wins = {}


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
        if source_name != "No file selected":
            print(source_name)
            print(type(source_name))
            if path.isfile(source_name):
                read_file()
                for name in type1_init_max:
                    mutant = type1_init_max[name][0]
                    mutant_wins[mutant] += 1
 #               print(mutant_wins)
            else:
                label.config(text="File not found. Try again?")





def read_file():
    ### call global variables
    global source_name
    global type1_init_max

    infile = open(source_name, "r")
    metadata = infile.readline()

    analysis_columns = check_metadata(metadata)

    if len(analysis_columns) > 0:
        line_counter = 1
        for line in infile:
            if line_counter > 1:
#                print(line)
                analyze_line(line, analysis_columns)

            line_counter += 1

#        print(len(type1_init_max))



def check_metadata(metaline):
    global required_columns
    empty_loc = {}
    col_loc = {}
    metacols = metaline.split("\t")

    for name in required_columns:
        if name not in metacols:
            return(empty_loc)
        else:
            col_loc[name] = metacols.index(name)
    print(col_loc)
    return(col_loc)


def analyze_line(dataline, data_cols):
    global type1_init_max
    global mutant_wins

    data = dataline.split("\t")
    if len(data) < 2:
        return

    type1_name = data[data_cols["type1Name"]]

    mutant = data[data_cols["mutant"]]
    if mutant not in mutant_wins:
        mutant_wins[mutant] = 0

    try_max = list((mutant, data[data_cols["MT initiation Tm"]]))

    if type1_name in type1_init_max:
        if data[data_cols["MT initiation Tm"]] > type1_init_max[type1_name][1]:
            type1_init_max[type1_name] = try_max
    else:
        type1_init_max[type1_name] = try_max






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

#    results_frame = Frame(root, bd=7, bg=background)
#    results_frame.pack()


    root.mainloop()


if __name__ == "__main__":
    start()
