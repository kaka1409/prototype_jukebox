import pytest
from unittest.mock import patch, ANY
import tkinter as tk
from src import MainMenu

@pytest.fixture
def main_menu():
    """Create and destroy a Tk window with MainMenu for testing"""

    root = tk.Tk()
    menu = MainMenu(root)
    yield menu  # provide the fixture value to the test
    root.destroy()

def test_initialization(main_menu):
    """Test if MainMenu initializes with correct window properties"""

    main_menu.main_window.update_idletasks()  # force window to update size
    geometry_value = main_menu.main_window.winfo_geometry()  # get geometry value
    dimensions = geometry_value.split('+')[0]  # get widthxheight

    # Check if window properties are set correctly
    assert main_menu.main_window.title() == "JukeBox"
    assert dimensions == "480x320"
    assert main_menu.main_window.cget('bg') == "gray"

def test_button_existence(main_menu):
    """Test if all required buttons exist"""

    assert isinstance(main_menu.view_tracks_btn, tk.Button)
    assert isinstance(main_menu.create_track_list_btn, tk.Button)
    assert isinstance(main_menu.update_track_btn, tk.Button)

def test_button_text(main_menu):
    """Test if buttons have correct text"""

    assert main_menu.view_tracks_btn['text'] == "View Tracks"
    assert main_menu.create_track_list_btn['text'] == "Create Track List"
    assert main_menu.update_track_btn['text'] == "Update Tracks"

def test_label_existence(main_menu):
    """Test if labels exist and have correct initial state"""

    assert isinstance(main_menu.header_lbl, tk.Label)
    assert isinstance(main_menu.status_lbl, tk.Label)
    assert main_menu.status_lbl['text'] == "Welcome, This is the main menu"

@patch('src.track_player.TrackViewer')  # Mock TrackViewer in track_player
def test_view_tracks_button_click(mock_track_viewer, main_menu):
    """Test view tracks button click behavior"""

    main_menu.run_view_tracks()

    # Check if the status label is updated as expected
    assert main_menu.status_lbl['text'] == "View Tracks button was clicked!"

    # Verify that TrackViewer was called with a Toplevel window
    mock_track_viewer.assert_called_once_with(ANY)

@patch('src.track_player.CreateTrack')
def test_create_track_button_click(mock_create_track, main_menu):
    """Test create track button click behavior"""
    main_menu.run_create_track()

    # Check if the status label is updated as expected
    assert main_menu.status_lbl['text'] == "Update Tracks button was clicked!"

    # Verify that CreateTrack was called with a Toplevel window
    mock_create_track.assert_called_once_with(ANY)

@patch('src.track_player.UpdateTrack')
def test_update_track_button_click(mock_update_track, main_menu):
    """Test update track button click behavior"""
    main_menu.run_update_track()

    # Check if the status label is updated as expected
    assert main_menu.status_lbl['text'] == "Update Tracks button was clicked!"

    # Verify that UpdateTrack was called with a Toplevel window
    mock_update_track.assert_called_once_with(ANY)
