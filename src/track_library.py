import pandas as pd

from src.library_item import LibraryItem
from tkinter import messagebox

data = pd.read_csv('assets/songs.csv') # get song info from csv file
library = {} # init dictionary to store song objects

for index, row in data.iterrows(): # loop through each row

    library[f"0{row['id']}"] = LibraryItem (
        f"{row['name']}", # string
        f"{row['artist']}", # string
        row['rating'], # integer
        f"{row['path']}" # string
    )

# GETTER

def get_name(key):
    try:
        item = library[key]
        return item.name
    except KeyError:
        return None
    
def get_artist(key):
    try:
        item = library[key]
        return item.artist
    except KeyError:
        return None
    
def get_rating(key):
    try:
        item = library[key]
        return item.rating
    except KeyError:
        return None
    
def get_play_count(key):
    try:
        item = library[key]
        return item.play_count
    except KeyError:
        return -1

# SETTER

def set_rating(key, rating):
    try:
        item = library[key]
        item.rating = rating
    except KeyError:
        return 

# ACT

def list_all():
    output = ""

    for key in library:
        item = library[key]
        output += f"{key} {item.info()} \n"
        
    return output

def increment_play_count(key):
    try:
        item = library[key]
        item.play_count += 1
    except KeyError:
        return

def validate_input(input):

    try:
        integer_input = int(input)

        if integer_input < 1 or integer_input > len(library):
            messagebox.showerror("Error", f"Song ID is not found (currently from 1 to {len(library)})")
            return None
    
    except ValueError:

        if (input == ""):
            messagebox.showerror("Error", "Input must not be empty")
            return None

        messagebox.showerror("Error", "Input must be number only")
        return None

    return "0" + str(integer_input)
