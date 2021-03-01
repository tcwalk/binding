#!/usr/bin/python

from tkinter import *
from tkinter import font
from tkinter import Scrollbar
import tkinter as tk
from tkinter.filedialog import askopenfile, askdirectory
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
    label.config(text=source.name)


def count_binding(sel_label, binding_label, wins_label):
    ### call global variables
    global source_name
    global type1_init_max
    global mutant_wins
    type1_init_max= {}
    mutant_wins = {}

    if source_name is not None:
        if source_name != "No file selected":
            print(source_name)
            print(type(source_name))
            if path.isfile(source_name):
                read_file()
                if len(type1_init_max) > 0:
                    for name in type1_init_max:
                        mutant = type1_init_max[name][0]
                        mutant_wins[mutant] += 1

                    max_table = prep_max_table()
                    wins_table = prep_wins_table()
                    binding_label.config(text=max_table)
                    wins_label.config(text=wins_table)
                else:
                    binding_label.config(text="File format not supported")
                    wins_label.config(text="Try again?")

            else:
                sel_label.config(text="File not found. Try again?")


def prep_max_table():
    global type1_init_max

    max_table = "Type1\tmutant\tMT initiation Tm\n"

    for name in sorted(type1_init_max.keys()):
        mutant = type1_init_max[name][0]
        binding = type1_init_max[name][1]
        max_table = max_table + name + "\t" + mutant + "\t  " + str(binding) + "\n"

    return(max_table)

def prep_wins_table():
    global mutant_wins
    wins_table = "mutant\twins\n"

    for mutant in sorted(mutant_wins.keys()):
        wins = mutant_wins[mutant]
        wins_table = wins_table + mutant + "\t  " + str(wins) + "\n"

    return(wins_table)




def read_file():
    ### call global variables
    global source_name, type1_init_max, required_columns

    infile = open(source_name, "r")
    metadata = infile.readline()

    analysis_columns = check_metadata(metadata)

    if len(analysis_columns) == len(required_columns):
        line_counter = 1
        for line in infile:
            if line_counter > 1:
#                print(line)
                analyze_line(line, analysis_columns)

            line_counter += 1
    infile.close()
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



def print_results():
    global type1_init_max
    global mutant_wins

    max_table = prep_max_table()
    wins_table = prep_wins_table()

    out_dir = askdirectory(title='Please select output directory')

    max_out_file = out_dir + "/type1_init_max.tsv"
    wins_out_file = out_dir + "/binding_wins.tsv"

    outfile_max = open(max_out_file, "w")
    outfile_max.write(max_table)

    outfile_wins = open(wins_out_file, "w")
    outfile_wins.write(wins_table)

    outfile_max.close()
    outfile_wins.close()


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

    ### Select file here. Use lambda to pass label for updating as argument
    src_frame = Frame(root, bd=7, bg=background)
    src_frame.pack()
    src_file_button = Button(src_frame, bg=button_background, text='CHOOSE FILE', command=lambda:choose_file(selected_label))
    src_file_button.pack(side="top", pady=10)

    start_btn = Button(src_frame, text='Run Analysis', command=lambda:count_binding(selected_label, max_binding_label, binding_wins_label))
    start_btn.pack(side="left", padx=10, pady=10)
    print_btn = Button(src_frame, text='Print Results', command=print_results)
    print_btn.pack(side="left", padx=10, pady=10)
    close_btn = Button(src_frame, bg=button_background, text='Exit', command=lambda: sys.exit())
    close_btn.pack(side="right", padx=10, pady=10)

#    spacer_frame = Frame(root, bd=7, bg=background)
#    spacer_frame.pack()
#    spacer_label = Label(spacer_frame, bg=background, width=60, anchor="w",
#                    text="============================================")

    max_binding_frame = Frame(root, bd=7, height=15, bg=background)
    max_binding_canvas = Canvas(max_binding_frame)
    max_binding_sb = Scrollbar(max_binding_frame, orient="vertical", command=max_binding_canvas.yview)
    max_scrollable_frame = Frame(max_binding_canvas)

    max_scrollable_frame.bind(
        "<Configure>",
        lambda e: max_binding_canvas.configure(
            scrollregion=max_binding_canvas.bbox("all")
        )
    )

    max_binding_canvas.create_window((0, 0), window=max_scrollable_frame, anchor="nw")
    max_binding_canvas.configure(yscrollcommand=max_binding_sb.set)
    max_binding_label = Label(max_scrollable_frame, bg=background, text="Max binding data will appear here")
    max_binding_frame.pack()
    max_binding_canvas.pack(side="left", fill="both", expand=True)
    max_binding_sb.pack(side="right",fill="both")
    max_binding_label.pack(side="top")


    binding_wins_frame = Frame(root, bd=7, height=15, bg=background)
    binding_wins_canvas = Canvas(binding_wins_frame)
    binding_wins_sb = Scrollbar(binding_wins_frame, orient="vertical", command=binding_wins_canvas.yview)
    wins_scrollable_frame = Frame(binding_wins_canvas)

    wins_scrollable_frame.bind(
        "<Configure>",
        lambda e: binding_wins_canvas.configure(
            scrollregion=binding_wins_canvas.bbox("all")
        )
    )

    binding_wins_canvas.create_window((0, 0), window=wins_scrollable_frame, anchor="nw")
    binding_wins_canvas.configure(yscrollcommand=binding_wins_sb.set)
    binding_wins_label = Label(wins_scrollable_frame, bg=background, text="Binding wins data will appear here")
    binding_wins_frame.pack()
    binding_wins_canvas.pack(side="left", fill="both", expand=True)
    binding_wins_sb.pack(side="right",fill="both")
    binding_wins_label.pack(side="top")





    root.mainloop()


if __name__ == "__main__":
    start()
