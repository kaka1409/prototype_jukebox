import pytest 
import tkinter as tk
from unittest.mock import patch

from src import TrackViewer

@pytest.fixture
def mock_window():
    window = tk.Tk()
    yield window
    window.destroy()

@pytest.fixture
def view_track_window(mock_window): # mock window
    return TrackViewer(mock_window) # create the view track window

class TestTrackViewer():
    def test_init(self, view_track_window, mock_window):
        
        # test title
        assert mock_window.title() == "View Tracks"

        mock_window.update_idletasks()
        geometry_value = mock_window.geometry()
        width_and_height = geometry_value.split('+')[0]

        assert width_and_height == "750x350"

        # test if widget is created as expected
        assert isinstance(view_track_window.list_tracks_btn, tk.Button)
        assert isinstance(view_track_window.enter_lbl, tk.Label)
        assert isinstance(view_track_window.check_track_btn, tk.Button)
        assert isinstance(view_track_window.input_lbl, tk.Label)
        assert isinstance(view_track_window.input_txt, tk.Entry)
        assert isinstance(view_track_window.list_txt, tk.scrolledtext.ScrolledText)
        assert isinstance(view_track_window.track_txt, tk.Text)
        assert isinstance(view_track_window.status_lbl, tk.Label)
    
    # test list all track function
    @patch('src.track_library.list_all')
    def test_list_all_tracks_function(self, mock_list_all, view_track_window):
        
        test_text = "Track 1\nTrack 2\nTrack 3"
        mock_list_all.return_value = test_text # set the list all function to return a specific value
        
        # simulate click event of list_tracks button
        view_track_window.list_tracks_clicked()

        assert view_track_window.list_txt.get("1.0", tk.END).strip() == test_text
        assert view_track_window.status_lbl["text"] == "List Tracks button was clicked"

    # test view track button when
    # Test view_tracks_clicked function with valid input
    @patch('src.track_library.get_name', return_value = "Test Track")
    @patch('src.track_library.get_artist', return_value = "Test Artist")
    @patch('src.track_library.get_rating', return_value = 4)
    @patch('src.track_library.get_play_count', return_value = 150)
    @patch('src.track_library.validate_input')

    def test_view_track_valid_input(self, 
            mock_validate, mock_get_name, 
            mock_get_artist, mock_get_rating, 
            mock_get_play_count, view_track_window
        ):

        """
        Test the view_tracks_clicked function when valid inputs are entered.
        Expected behavior:
        - track_txt should display the correct track details.
        - status_lbl should indicate that the "View Tracks Button was clicked".
        """

        # Define valid inputs and the expected output
        valid_inputs = ["1", "01", "00000001"]
        expected_output = "Test Track \n Test Artist \n rating: 4 \n plays: 150"
        
        # Loop through each valid input
        for valid_input in valid_inputs:
            
            # Mock validate_input to return a standardized track ID for each valid input
            mock_validate.return_value = "01"
            
            # Set the valid input in the input field
            view_track_window.input_txt.insert(0, valid_input)
            
            # Simulate click event of view_tracks button
            view_track_window.view_tracks_clicked()
            
            # Check if track details are displayed correctly
            assert view_track_window.track_txt.get("1.0", tk.END).strip() == expected_output
            assert view_track_window.status_lbl["text"] == "View Tracks Button was clicked"
            
            # Clear the input and track_txt fields for the next test case
            view_track_window.input_txt.delete(0, tk.END)
            view_track_window.track_txt.delete("1.0", tk.END)


    # Test view_tracks_clicked function with invalid input
    @patch('tkinter.messagebox.showerror')
    @patch('src.track_library.validate_input', return_value=None)

    def test_view_track_invalid_input(self, mock_validate, mock_showerror, view_track_window):
        
        """SET UP TEST INPUTS"""
    
        invalid_inputs = [
            ("348957", "Song ID is not found (currently from 1 to 5)"),  # Out of range
            ("one", "Input must be number only"),                        # Non-numeric
            ("", "Input must not be empty"),                             # Empty
            ("   ", "Input must not be empty"),                          # Whitespace only
            ("$@0 01yes", "Input must be number only"),                  # Special characters
        ]

        """TEST INPUTS STRUCTURE"""

        """
        invalid_inputs = [
            ("invalid input", "expected message")
        ]

        appropriate error message should be displayed accordingly to the invalidation of the input
        """

        for input_value, expected_message in invalid_inputs:

            # Set the invalid input in the input field
            view_track_window.input_txt.delete(0, tk.END)  # Clear any existing text
            view_track_window.input_txt.insert(0, input_value)  # Insert invalid input
            
            # Simulate click event of view_tracks button
            view_track_window.view_tracks_clicked()

            # Check if track text area is empty and status label is updated
            assert view_track_window.track_txt.get("1.0", tk.END).strip() == ""
            assert view_track_window.status_lbl["text"] == "View Tracks Button was clicked"

            # Verify that messagebox.showerror was called with the correct error message
            mock_showerror.assert_called_once_with("Error", expected_message)
            
            # Reset the mock for the next test case
            mock_showerror.reset_mock()


