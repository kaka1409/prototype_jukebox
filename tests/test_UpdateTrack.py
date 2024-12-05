"""UNIT TESTING UPDATE TRACK"""

"""
- testing find track button (check when clicking the button)
if the input is valid (should set up a list of valid inputs):
+ has the status been updated correctly?
+ has the song's info been displayed correctly?
if the input is invalid (should set up a list of invalid inputs)
+ has appropriate messageboxs appeared?

- testing update track button (check when clicking the button)
if the input is valid (should set up a list of valid inputs):
+ has the status been updated correctly?
+ has the new rating been displayed correctly?
if the input is invalid (should set up a list of invalid inputs)
+ has appropriate messageboxs appeared?

"""
import pytest
from unittest.mock import MagicMock
import tkinter as tk

from src.track_library import library
from src import library_method
from src import UpdateTrack

# mock library data
mock_data = {
    "01": MagicMock (
        name = "song-1",
        artist = "Artist-1",
        rating = 3,
        play_count = 5,
        path = "https://youtube/song-1"           
    ),

    "02": MagicMock (
        name = "song-2",
        artist = "Artist-2",
        rating = 5,
        play_count = 15,
        path = "https://youtube/song-2"           
    ),

    "03": MagicMock (
        name = "song-3",
        artist = "Artist-3",
        rating = 2,
        play_count = 2,
        path = "https://youtube/song-3"           
    )
}


# create the update track window 
@pytest.fixture
def update_track_window(mocker):
    """create update_track window for tesing"""

    window = tk.Tk()
    update_track = UpdateTrack(window)

    # targeting the library data and messagebox (mocking lib data and msgbox)
    mocker.patch.dict(library, mock_data)
    mock_messagebox = mocker.patch("src.update_track.messagebox.showerror")
    return update_track, mock_messagebox 

    

def test_find_track_button_valid(update_track_window):
    """Testing find track button with valid inputs"""

    update_track, mock_messagebox = update_track_window

    # set up a list of valid_input
    valid_inputs = ["1", "02", "000000003", " 0 0004", "   00 0 00  0005"]

    for valid_input in valid_inputs:

        # add the input to the entry
        update_track.find_track_input.delete(0, tk.END)
        update_track.find_track_input.insert(0, valid_input)

        # click the find track button
        update_track.get_track()

        # simulate get user input mechanic
        input_key = valid_input.replace(" ", "")

        # validate input
        key = library_method.validate_input(input_key)

        expected_text = str(library[key].info()) # get the info
        displayed_text = update_track.selected_song_text_area.get("1.0", tk.END).strip() # get text from update track window

        # check if the status was displayed correctly
        assert update_track.status['text'] == "Your track has been found"

        # check if the song was displayed correctly
        assert displayed_text == expected_text


def test_find_track_button_invalid(update_track_window):
    """Test the find track button with invalid inputs and check whether the messagebox has been called"""

    update_track, mock_messagebox = update_track_window

    # assert update_track is not None
    # assert mock_messagebox is not None

    # set up a list of invalid inputs
    invalid_inputs = ["992982213", "", "     ", "one", "01a&#"]
    """ invalid_inputs = [out of range, empty string, whitespace only, has alplahetical characters, has special characters ] """

    for invalid_input in invalid_inputs:

        # add the input to the entry
        update_track.find_track_input.delete(0, tk.END)
        update_track.find_track_input.insert(0, invalid_input)

        update_track.get_track()

        # check if messagebox has called
        mock_messagebox.assert_called()
        
def test_update_track_button_valid_inputs(update_track_window):
    """Test the update track button with valid new rating inputs."""

    update_track, mock_messagebox = update_track_window
    valid_inputs = [("1", 4), ("2", 5)]

    for input_id, new_rating in valid_inputs:

        # Set up the selected track
        update_track.find_track_input.delete(0, tk.END)
        update_track.find_track_input.insert(0, input_id)
        update_track.get_track()

        # Update the new rating input and simulate the button click
        update_track.input_new_rating.delete(0, tk.END)
        update_track.input_new_rating.insert(0, str(new_rating))
        update_track.update_rating()

        # Check if status label was updated correctly
        assert update_track.status["text"] == "The song has been given a new rating"

        # Check if the new rating is displayed correctly in the output area
        selected_key = f"0{input_id}"
        updated_text = update_track.display_track_new_rating.get("1.0", tk.END).strip()
        assert updated_text == str(library[selected_key].info())

def test_update_track_button_invalid_inputs(update_track_window):
    """Test the update track button with invalid new rating inputs and check for messagebox calls."""
    update_track, mock_messagebox = update_track_window

    # Set up valid track selection
    update_track.find_track_input.delete(0, tk.END)
    update_track.find_track_input.insert(0, "1")
    update_track.get_track()

    invalid_ratings = ["", "abc", "6", "0"]

    for invalid_rating in invalid_ratings:
        # Set invalid rating input and simulate the update button click
        update_track.input_new_rating.delete(0, tk.END)
        update_track.input_new_rating.insert(0, invalid_rating)
        update_track.update_rating()

        # Check if messagebox.showerror was called
        mock_messagebox.assert_called()


    

     