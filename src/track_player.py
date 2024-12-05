import tkinter as tk

import src.font_manager as fonts
from src.view_track import TrackViewer
from src.update_track import UpdateTrack
from src.create_track_list import CreateTrackList

class MainMenu():
    def __init__(self, window):

        # initilize main menu  
        self.main_window = window
        window.title("JukeBox")
        window.geometry("480x320")
        window.configure(bg = "gray")
        

        self.header_lbl = tk.Label(
            window,
            text = "Select an option by clicking one of the button below"
        )
        self.header_lbl.grid(
            row = 0,
            column = 0,
            columnspan = 3,
            padx = 10,
            pady = (10, 50)
        )

        self.view_tracks_btn = tk.Button(
            window,
            text = "View Tracks",
            command = self.run_view_tracks
        )
        self.view_tracks_btn.grid(
            row = 1,
            column = 1,
            padx = 10,
            pady = 10
        )

        self.create_track_list_btn = tk.Button(
            window,
            text = "Create Track List",
            command = self.run_create_track
        )
        self.create_track_list_btn.grid(
            row = 2,
            column = 1,
            padx = 10,
            pady = 10
        )

        self.update_track_btn = tk.Button(
            window,
            text = "Update Tracks",
            command = self.run_update_track
        )
        self.update_track_btn.grid(
            row = 3,
            column = 1,
            padx = 10,
            pady = 10
        )

        #status
        self.status_lbl = tk.Label(
            window,
            bg = 'gray',
            text = "Welcome, This is the main menu",
            font = ("Helvetica", 10)
        )
        self.status_lbl.grid(
            row = 4,
            column = 0,
            columnspan = 3,
            padx = 10,
            pady = 10
        )

    def run_view_tracks(self):
        self.status_lbl.configure(text = "View Tracks button was clicked!")
        TrackViewer(tk.Toplevel(self.main_window))

    def run_create_track(self):
        self.status_lbl.configure(text = "Update Tracks button was clicked!")
        CreateTrackList(tk.Toplevel(self.main_window))

    def run_update_track(self):
        self.status_lbl.configure(text = "Update Tracks button was clicked!")
        UpdateTrack(tk.Toplevel(self.main_window))

    def run():
        window = tk.Tk()
        fonts.configure()
        MainMenu(window)
        window.mainloop()
