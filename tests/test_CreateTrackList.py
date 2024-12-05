"""UNIT TESTING CREATE PLAYLIST FUNCTIONALITY"""

"""
test inputs: 
+ set up a list of valid and invalid inputs
+ check when entering inputs the appropriate status shoud be updated
+ check whenever the input is invalid the appropriate message box should be displayed

test add button: when clicking the add button check
+ has the status been updated?
+ has the track been added to the playlist?
+ has the playlist display the selected song?

test play button: when clicking the play button check
+ has the playcount of the song in the playlist been increased?
+ has the status been updated?

test reset button: when clicking the reset button check
+ has the playlist been reseted?
+ has the status been updated?

"""

import pytest
from unittest.mock import patch
import tkinter as tk

from src import CreateTrackList
from src.track_library import library, validate_input


@pytest.fixture
def app():
    """Set up the CreateTrack app instance for testing."""
    root = tk.Tk()
    app = CreateTrackList(root)
    return app


@patch("tkinter.messagebox.showerror")
def test_input_validation(mock_showerror, app):
    """Test various valid and invalid inputs."""

    # Test valid inputs
    valid_inputs = ["1", "02", "0000003"]

    for input_value in valid_inputs:
        assert validate_input(input_value) is not None  # Should return a valid song key

    # Test invalid inputs
    invalid_inputs = [
        ("9999", "Song ID is not found (currently from 1 to 5)"),   # Out of range
        ("two", "Input must be number only"),                       # Non-numeric
        ("", "Input must not be empty"),                            # Empty
    ]

    # test if the messagebox appear
    for input_value, expected_message in invalid_inputs:

        app.add_song_input.delete(0, tk.END)
        app.add_song_input.insert(0, input_value)
        app.add_song()  # Trigger add_song with invalid input
        
        mock_showerror.assert_called_once_with("Error", expected_message)
        mock_showerror.reset_mock()  # Reset for next test case

def test_add_song_button(app):
    """Test the add song button functionality."""
    
    valid_input = "1"  # Assuming "1" is a valid ID in `library`

    # Set valid input in the entry box
    app.add_song_input.delete(0, tk.END)
    app.add_song_input.insert(0, valid_input)

    # Add the song to the playlist
    app.add_song()

    # Check if status is updated correctly
    assert app.status.cget("text") == "Your song has been added"

    # Check if the song is in the playlist display
    song_info = library["01"].info()  # Assuming the key is formatted with leading zero
    assert song_info in app.playlist.get("1.0", tk.END)

@patch("webbrowser.open")
@patch("src.track_library.increment_play_count")
def test_play_button(mock_increment, mock_open, app):
    """Test the play button functionality."""

    # Add a valid song to the playlist
    app.storeSongKey.append("01")  # Assuming "01" is a valid key in the library

    # Click the play button
    app.play()

    # Verify play count increment and web browser opening
    mock_increment.assert_called_once_with("01")
    mock_open.assert_called_once_with(library["01"].path)  # Open song URL

    # Check if status is updated correctly
    assert app.status.cget("text") == "Your playlist is playing now"

def test_reset_button(app):
    """Test the reset button functionality."""
    
    # Add a song to the playlist and set the status
    app.storeSongKey.append("01")  # Assuming "01" is a valid key in the library
    app.playlist.insert("1.0", library["01"].info())  # Add song info

    # Click the reset button
    app.reset_playlist()

    # Check if playlist and status are updated
    assert app.playlist.get("1.0", tk.END).strip() == ""  # Playlist should be empty
    assert app.status.cget("text") == "Reset button has been clicked"