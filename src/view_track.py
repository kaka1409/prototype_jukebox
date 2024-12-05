import tkinter as tk
import tkinter.scrolledtext as tkst

import src.track_library as library
from src.track_library import validate_input

def set_text(text_area, content): #insert content into the text area
    text_area.delete("1.0", tk.END) #first the existing content is deleted
    text_area.insert(1.0, content) #then the new content is inserted

class TrackViewer(): # define the class TrackViewer

    def __init__(self, window): # define the constructor of the class TrackViewer

        window.geometry("750x350") # set the width x height of the main window to be 750 x 350
        window.title("View Tracks") # set the title of the application as "View Tracks"

        self.list_tracks_btn = tk.Button( # create the widget button to list out all the tracks
            window, # place the widget on the main window 
            text = "List All Tracks", # set the text displayed on the button to "List All Tracks"
            command = self.list_tracks_clicked # call the function list_tracks_clicked() whenever the button is clicked
        )
        self.list_tracks_btn.grid( # using grid to manage the position of the list out button
            row = 0, # set the list_track button to belong to row 0
            column = 0, # set the list_track button to belong to column 0
            padx = 10, # set the padding on x-axis to 10 pixel
            pady = 10 # set the padding on y-axis to 10 pixel
        )

        self.enter_lbl = tk.Label( # create the the label widget for entering track number
            window, # place the widget on the main window
            text = "Enter Track Number" # set the title of the application as "Enter Track Number"
        )
        self.enter_lbl.grid( # using grid to manage the position of the enter label
            column = 1, # set the label to belong to row 0
            padx = 10,  # set the padding on x-axis to 10 pixel
            pady= 10 # set the padding on y-axis to 10 pixel
        )

        self.check_track_btn = tk.Button( # create the the button widget for viewing tracks
            window, # place the widget on the main window
            text = "View Track", # set the text of the button to "View track"
            command = self.view_tracks_clicked # call the view_tracks_cliked() function whenever the button is clicked
        )
        self.check_track_btn.grid( # using grid to manage the position of the view track button
            row = 0, # set the view track button to belong to row 0
            column = 3, # set the view track button to belong to column 3
            padx = 10, # set the padding on x-axis to 10 pixel
            pady = 10 # set the padding on y-axis to 10 pixel
        )

        self.input_lbl = tk.Label( # create the the Label widget for the input text
            window, # place the widget on the main window
            text = "Enter track ID" # set the text of the label to "Enter track ID"
        )
        self.input_lbl.grid( # using grid to manage the position of the input label
            row = 0, # set the view track button to belong to row 1
            column = 1, # set the view track button to belong to column 1
            padx = 10, # set the padding on x-axis to 10 pixel
            pady = 10 # set the padding on y-axis to 10 pixel
        )

        self.input_txt = tk.Entry( # create the the entry widget for the input text
            window, # place the widget on the main window
            width = 3 # set the width of the input text to be 3
        )
        self.input_txt.grid( # using grid to manage the position of input text
            row = 0, # set the input text to belong to row 0
            column = 2, # set the input text to belong to column 0
            padx = 10, # set the padding on x-axis to 10 pixel
            pady = 10 # set the padding on y-axis to 10 pixel
        )

        self.list_txt = tkst.ScrolledText( # create the the text area widget for displaying a list of all the tracks
            window, # place the widget on the main window
            width = 48, # set the width of the text area to 48 pixel
            height = 12, # set the height of the text area to 12 pixel
            wrap = "none", # disable wrap
        )
        self.list_txt.grid( # using grid to manage the position of text area
            row = 1, # position the text area to row 1
            column = 0, # position the text area to column 0
            columnspan = 3, # let the text area to span out to 3 column
            sticky = "W", # set the text area to stcik to West - left
            padx = 10, # set the padding on x-axis to 10 pixel
            pady = 10 # set the padding on y-axis to 10 pixel
        )

        self.track_txt = tk.Text( # create the the text widget
            window, # place the widget on the main window
            width = 24, # set the width of the text to 24 pixel
            height = 4, # set the height of the text to 4 pixel
            wrap = "none" # disable wraping
        )
        self.track_txt.grid( # using grid to manage the position of
            row = 1, # position the text to row 1
            column = 3, # position the text to column 3
            sticky = "NW", # set the text stick to North West
            padx = 10, # set the padding on x-axis to 10 pixel
            pady = 10 # set the padding on y-axis to 10 pixel
        )

        self.status_lbl = tk.Label( # create the the label widget for the status 
            window, # place the widget on the main window
            text = "", # set the text to be an empty string
            font = ("Helvatica", 10) # set the font of the status to be "Helvatica" with the font size as 10
        )
        self.status_lbl.grid( # using grid to manage the position of the status 
            row = 2,  # position the label to row 2
            column = 0, # position the label to column 0
            columnspan = 4, # let the label to span across 4 column
            sticky = "W", # set the label stick to West
            padx = 10,  # set the padding on x-axis to 10 pixel
            pady = 10 # set the padding on y-axis to 10 pixel
        )

        self.list_tracks_clicked()

    def view_tracks_clicked(self): #define the view_tracks_clicked() function

        input_key = self.input_txt.get().replace(" ", "") # assign the value of the input text to variable key
        key = validate_input(input_key) # validate user input
        name = library.get_name(key) # find the name of the track (assign the name to the name variable)
        
        self.status_lbl.configure(text = "View Tracks Button was clicked") # change the status whenever the view_track button is clicked
        
        if key == None : return # exit the function if key is None

        if name is not None: # if the name of the track is found then 

            artist = library.get_artist(key) # get the artist name
            rating = library.get_rating(key) # get the rating of the track
            play_count = library.get_play_count(key) # get the play count of the track
            track_details = f"{name} \n {artist} \n rating: {rating} \n plays: {play_count}" # assign the detail of the track (name, artist, rating and play count) to a variable for displaying
            set_text(self.track_txt, track_details) # call the set_text() function to set the text in the displaying area as the info of the track

        else:
            set_text(self.track_txt, f"Track {key} was not found") # if the name is not found call set_text() function to display error

    def list_tracks_clicked(self): # define the list_tracks_clicked() function

        self.status_lbl.configure(text = "List Tracks button was clicked") # set the status whenever the list all button is clicked

        track_list = library.list_all() # get the info all of the tracks
        set_text(self.list_txt, track_list) # set the text to display all of the tracks (the whole list)
