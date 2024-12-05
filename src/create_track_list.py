import webbrowser
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox

import src.track_library as lib
from src.track_library import library
from src.track_library import validate_input

class CreateTrackList():
    def __init__(self, window):
        
        window.geometry("1200x800")
        window.title("Create Track List")

        # frame to contain the header
        self.heading = tk.Frame(
            window,
            bg = "#E4E4E4",
        )
        self.heading.pack(
            fill = 'x',
            side = "top",
            padx = 10,
        )

        self.heading_title = tk.Label(
            self.heading,
            text = "Create your playlist",
            font = ("Helvetica", 15)
        )
        self.heading_title.pack(
            pady = 15
        )

        #frame to contain all the buttons
        self.button_container = tk.Frame(
            window,
            bg = "#E4E4E4",
        )
        self.button_container.pack(
            fill = 'y',
            side = "left",
            padx = 10,
            pady = (20, 0)
        )

        # add song to playlist (display error if song is not found)

        #button
        self.add_song_btn = tk.Button(
            self.button_container,
            text = "Add song",
            width = 8,
            font = ("Helvetica", 12),        
            command = self.add_song
        )
        self.add_song_btn.grid(
            row = 0,
            column = 0,
            padx = 10,
            pady = (15, 10)
        )

        #Entry (input here)
        self.add_song_input = tk.Entry(
            self.button_container,
            width = 8,
        )
        self.add_song_input.grid(
            row = 1,
            column = 0,
            padx = 10,
            pady = (10, 50),
        )

        # play the playlist button (play_count in each song of the playlist should be + 1)

        # play button
        self.play_btn = tk.Button(
            self.button_container,
            text = "Play",
            width = 8,
            font = ("Helvetica", 12),
            command = self.play
        )
        self.play_btn.grid(
            row = 2,
            column = 0,
            padx = 10,
            pady = 10
        )

        # reset the playlist

        self.reset_btn = tk.Button(
            self.button_container,
            text = "Reset",
            width = 8,
            font = ("Helvetica", 12),
            command = self.reset_playlist
        )
        self.reset_btn.grid(
            row = 3,
            column = 0,
            padx = 10,
            pady = 10
        )

        # main frame to contain both the playlist and available song
        self.main_container = tk.Frame(
            window,
            bg = "#E4E4E4"
        )
        self.main_container.pack(
            padx = 10,
            pady = (20, 10),
            fill = "both",
            expand = True
        )

        # Configure column weights in main_container to ensure equal spacing
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        # frame to contain all available song
        self.available_list_container = tk.Frame(
            self.main_container,
            bg = "#E4E4E4"
        )
        self.available_list_container.grid(
            row = 0,
            column = 1,
            padx = 10,
            sticky = 'nsew'
        )

        # frame to contain the playlist
        self.playlist_container = tk.Frame(
            self.main_container,
            bg = "#E4E4E4"
        )
        self.playlist_container.grid(
            row = 0,
            column = 0,
            padx = 10,
            sticky = 'nsew'
        )

        # Add "Available songs" label
        self.available_title = tk.Label(
            self.available_list_container,
            text = "Available songs",
            font = ("Helvetica", 12),
            bg = "#E4E4E4"
        )
        self.available_title.grid(
            row = 0,
            column = 0,
            pady = 10,
            sticky = 'ew'  # Make label expand horizontally
        )

        # Modify playlist title
        self.playlist_title = tk.Label(
            self.playlist_container,
            text = "Your playlist",
            font = ("Helvetica", 12),
            bg = "#E4E4E4"
        )
        self.playlist_title.grid(
            row = 0,
            column = 0,
            pady = 10,
            sticky = 'ew'  # Make label expand horizontally
        )

        # Configure the label containers to center the text
        self.available_list_container.grid_columnconfigure(0, weight=1)
        self.playlist_container.grid_columnconfigure(0, weight=1)

        # Available songs list
        self.available_list = tkst.ScrolledText(
            self.available_list_container,
            width = 40,
            height = 30
        )
        self.available_list.grid(
            row = 1,
            column = 0,
            sticky = 'nsew'
        )

        # Playlist
        self.playlist = tkst.ScrolledText(
            self.playlist_container,
            width = 40,
            height = 30
        )
        self.playlist.grid(
            row = 1,
            column = 0,
            sticky = 'nsew'
        )

        # frame to contain the status label
        self.status_container = tk.Frame(
            self.main_container,
            bg = "#E4E4E4",
        )
        self.status_container.grid(
            row = 1,
            column = 0,
            columnspan = 2,
            sticky = "nsew",
            padx = 10,
            pady = (50, 10)
        )

        # status
        self.status = tk.Label(
            self.status_container,
            font = ("Poppins", 10),
            bg = "#E4E4E4",
            text = ""
        )
        self.status.pack()

        self.available_list.insert(1.0, lib.list_all()) # list all song as default
    
        self.storeSongKey = []

    # functionality

    def add_song(self):

        input_key = self.add_song_input.get().replace(" ", "")
        key = validate_input(input_key)

        key_list = self.storeSongKey
        playlist_area = self.playlist # scrolledText

        if (key == None): return

        if (key not in key_list): # if the key is not in the list it will be added and the song_obj must be defined
                
            key_list.append(key)
            playlist_area.delete("1.0", tk.END) # delete the old display (hasn't been updated)

            for key in reversed(key_list): # loop list from the end -> start

                song_obj = library[key]
                song_info = song_obj.info() + "\n"

                playlist_area.insert(1.0, song_info)
                
        # update status
        self.status.config(text = "Your song has been added")


    def play(self):

        keys = self.storeSongKey    

        if (keys == []):        

            # display error
            messagebox.showerror("Error", "Please add songs to your playlist")

            # display warning on status
            self.status.config(text = "Your playlist is empty, please add songs")

            # stop execution
            return
        
        else:

            for key in keys:

                # increase play count
                lib.increment_play_count(key)

                url = library[key].path # library[key] is song object, obj.path to get the url
                webbrowser.open(url)

            # update status
            self.status.config(text = "Your playlist is playing now")


    def reset_playlist(self):

        self.storeSongKey = []
        self.playlist.delete("1.0", tk.END)

        # update status
        self.status.config(text = "Reset button has been clicked")
