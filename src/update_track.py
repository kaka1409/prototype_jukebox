import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox

import src.track_library as libraryItem
from src.track_library import library 
from src.track_library import validate_input
import src.font_manager as fonts

class UpdateTrack():

    def __init__(self, window):

        window.geometry("850x500")
        window.title("Update Tracks")

        # title
        self.heading = tk.Label(
            window,
            text = "Update Tracks",
        )
        self.heading.grid(
            row = 0,
            column = 3
        )

        # find the track
        self.find_track_btn = tk.Button(
            window,
            text = "Find track",
            font = ("Helvatica", 12),
            command = self.get_track
        )
        self.find_track_btn.grid(
            row = 5,
            column = 3,
            padx = (80, 0),
            sticky = "W"
        )

        # input entry to find the track
        self.find_track_input = tk.Entry(
            window,
            width = 15,
        )
        self.find_track_input.grid(
            row = 5,
            column = 3,
            sticky = "E"
        )

        # text area to display song's detail
        self.selected_song_text_area = tk.Text(
            window,
            width = 25,
            height = 3,
        )
        self.selected_song_text_area.grid(
            row = 6,
            column = 3,
            sticky = "ew",
            padx = (80, 0)
        )
        
        # display all track info(name, artist, rating)
        self.available_track_title = tk.Label(
            window,
            text = "Track's info"
        )
        self.available_track_title.grid(
            row = 1,
            column = 1,
        )

        self.available_track_area = tkst.ScrolledText(
            window,
            width = 36,
            height = 20,
            wrap = "none"
        )
        self.available_track_area.grid(
            row = 4,
            column = 0,
            rowspan = 10,
            columnspan = 3,
            padx = (20, 10),
            pady = 10
        )

        self.display_track_new_rating = tk.Text(
            window,
            width = 36,
            height = 3,
            wrap = "none"
        )
        self.display_track_new_rating.grid(
            row = 11,
            column = 3,
            padx = (80, 0),
        )

        # update new rating

        # button
        self.update_rating_btn = tk.Button(
            window,
            text = "Update rating",
            font = ("Helvatica", 12),
            command = self.update_rating
        )
        self.update_rating_btn.grid(
            row = 10,
            column = 3,
            sticky = "W",
            padx = (80, 0),
        )

        # input new rating entry
        self.input_new_rating = tk.Entry(
            window,
            width = 15,
        )
        self.input_new_rating.grid(
            row = 10,
            column = 3,
            sticky = "E"
        )

        # status
        self.status = tk.Label(
            window,
            font = ("Poppins", 10),
            bg = "#E4E4E4",
            text = ""
        )
        self.status.grid(
            row = 14,
            column = 1,
            pady = (10, 0)
        )

        # placeholder text
        self.selected_song_text_area.insert("1.0", "Your selected song will be displayed here...")
        self.display_track_new_rating.insert("1.0", "Your song's new rating will be displayed here...")

        # set the placeholde text to gray
        self.selected_song_text_area.config(fg = "gray")
        self.display_track_new_rating.config(fg = "gray")

        # set the selected song as None as default since the user hasn't choose the song yet
        self.selected_song_key = None

        # list all track
        self.available_track_area.insert(1.0, libraryItem.list_all())

    # find track function
    def get_track(self):
        
        # get user input
        input_key = self.find_track_input.get().replace(" ", "")
        
        # validate the song ID
        key = validate_input(input_key) # return the key if the input is valid otherwise key will be None
        if (key == None): return
        
        self.selected_song_key = key
        
        selected_song_area = self.selected_song_text_area
        track = library[key]

        # display the selected song
        selected_song_area.delete("1.0", tk.END)
        selected_song_area.insert(1.0, track.info())
        selected_song_area.config(fg = "black")

        # update status
        self.status.config(text = "Your track has been found")

    # update rating function
    def update_rating(self):
        
        self.get_track()

        new_rating_str = self.input_new_rating.get().replace(" ", "")

        # validate the new rating input
        if (new_rating_str == ""):
            messagebox.showerror("Error", "Please enter the new rating")
            return 
        
        if list(filter(str.isalpha, new_rating_str)): # if the input contain characters error will be displayed
            messagebox.showerror("Error", "Rating must be number only")
            return 
        
        if (int(new_rating_str) < 1 or int(new_rating_str) > 5):
            messagebox.showerror("Error", "Rating must be a number between 1-5")
            return

        new_rating = int(new_rating_str)

        key = self.selected_song_key
        new_rating_area = self.display_track_new_rating
        available_area = self.available_track_area

        try:

            libraryItem.set_rating(key, new_rating)
            track_info = library[key]
            
            # display the song with new rating
            new_rating_area.delete("1.0", tk.END)
            new_rating_area.insert(1.0, track_info.info())
            new_rating_area.config(fg = "black")

            # update available song area
            available_area.delete("1.0", tk.END)
            available_area.insert(1.0, libraryItem.list_all())

            # update status
            self.status.config(text = "The song has been given a new rating")

        except:

            if(key == None):
                messagebox.showerror("Error", f"Please enter the song ID")
            