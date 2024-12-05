"""UNIT TESTING LIBRARY METHOD"""

"""
- Testing library dictionary:
+ has the data in the csv file been handled correctly?
+ has the dictionary constructed to what I has expected?

- when the key is valid:
+ get_name(), get_artist(), get_rating(), get_play_count() return the correct data
+ set_rating() actual change the rating
+ increment_play_count() actual increase the play_count of the song

- when the key is invalid
+ get_name(), get_artist(), get_rating(), get_play_count() return None as expected
+ set_rating() and increment_play_count() return empty as expected

- testing validate_input():
+ set up a list of valid inputs and invalid inputs
+ trying the list set up before and expecting appropriate messagebox to appear(
out of range, empty string, contain alphabetical and special characters)

"""

import pytest
from unittest.mock import patch

from src.track_library import (
    library,
    get_name,
    get_artist,
    get_rating,
    get_play_count,
    set_rating,
    increment_play_count,
    list_all,
    validate_input
)
from src.library_item import LibraryItem


# Mock data for CSV to simulate loading from 'assets/songs.csv'
MOCK_SONGS_DATA = [
    {
        "id": 1,
        "name": "Song1", 
        "artist": "Artist1",
        "rating": 5, 
        "path": "path/to/song1"
    },

    {
        "id": 2,
        "name": "Song2",
        "artist": "Artist2",
        "rating": 4,
        "path": "path/to/song2"
    },

    {
        "id": 3,
        "name": "Song3",
        "artist": "Artist3",
        "rating": 3,
        "path": "path/to/song3"
    },
]

@pytest.fixture(autouse = True)
def setup_mock_library():
    """Setup a mock library dictionary from the mock data."""

    global library
    library.clear()  # Clear any existing data

    for song in MOCK_SONGS_DATA:
        
        key = f"0{song['id']}"

        library[key] = LibraryItem(
            name = song["name"],
            artist = song["artist"],
            rating = song["rating"],
            path = song["path"]
        )

class TestLibraryFunctions:

    def test_library_initialization(self):
        """Test that the library dictionary is constructed correctly."""
        
        assert len(library) == len(MOCK_SONGS_DATA)

        for song in MOCK_SONGS_DATA:

            key = f"0{song['id']}"

            assert key in library
            assert library[key].name == song["name"]
            assert library[key].artist == song["artist"]
            assert library[key].rating == song["rating"]
            assert library[key].path == song["path"]

    def test_getters_with_valid_key(self):
        """Test getters (get_name, get_artist, get_rating, get_play_count) with a valid key."""
        key = "01"  # assuming '01' is a valid key

        assert get_name(key) == "Song1"
        assert get_artist(key) == "Artist1"
        assert get_rating(key) == 5
        assert get_play_count(key) == 0  # Assuming initial play_count is 0

    def test_setter_set_rating(self):
        """Test set_rating changes the rating as expected."""

        key = "01"
        
        set_rating(key, 2)

        assert get_rating(key) == 2

    def test_increment_play_count(self):
        """Test increment_play_count actually increases play_count."""

        key = "01"
        initial_count = get_play_count(key)

        increment_play_count(key)

        assert get_play_count(key) == initial_count + 1

    def test_getters_with_invalid_key(self):
        """Test getters (get_name, get_artist, get_rating, get_play_count) with an invalid key."""
        invalid_key = "999"  # Key that doesn't exist in the library

        assert get_name(invalid_key) is None
        assert get_artist(invalid_key) is None
        assert get_rating(invalid_key) is None
        assert get_play_count(invalid_key) == -1

    def test_setter_with_invalid_key(self):
        """Test set_rating and increment_play_count with an invalid key."""
        invalid_key = "999"  # Key that doesn't exist in the library

        # set_rating and increment_play_count should do nothing
        set_rating(invalid_key, 5)
        increment_play_count(invalid_key)

        # Since these methods don't return anything, we confirm by lack of errors
        # and that nothing in the library has changed unexpectedly
        assert len(library) == len(MOCK_SONGS_DATA)  # Ensure no new items were added

    @patch("tkinter.messagebox.showerror")
    def test_validate_input(self, mock_showerror):
        """Test validate_input with various valid and invalid inputs."""
        
        # Test valid inputs
        valid_inputs = ["1", "2", "3"]
        for input_value in valid_inputs:
            result = validate_input(input_value)
            assert result == f"0{input_value}"  # Valid IDs are prefixed with '0'
            mock_showerror.assert_not_called()  # No error should be shown for valid input

        # Test invalid inputs
        invalid_inputs = [
            ("6", f"Song ID is not found (currently from 1 to {len(library)})"),  # Out of range
            ("", "Input must not be empty"),  # Empty string
            ("abc", "Input must be number only"),  # Non-numeric input
            ("1!", "Input must be number only"),  # Special characters
        ]

        for input_value, expected_message in invalid_inputs:
            result = validate_input(input_value)

            assert result is None  # Invalid inputs should return None
            mock_showerror.assert_called_once_with("Error", expected_message)
            mock_showerror.reset_mock()  # Reset mock for next test case

    def test_list_all(self):
        """Test list_all returns a formatted list of all songs in the library."""
        expected_output = ""

        for song in MOCK_SONGS_DATA:
            key = f"0{song['id']}"
            song_info = library[key].info()  # Get info for each song
            expected_output += f"{key} {song_info} \n"
        
        assert list_all() == expected_output
