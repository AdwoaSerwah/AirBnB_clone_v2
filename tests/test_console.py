#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import os
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from console import HBNBCommand
import unittest
from unittest.mock import patch
import io


class TestHBNBCommand(unittest.TestCase):
    """"""
    def test_preloop_non_interactive(self):
        """Test that (hbnb) is printed in non-interactive mode."""
        with patch('sys.__stdin__.isatty', return_value=False):
            with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                console = HBNBCommand()
                console.preloop()
                self.assertEqual(mock_stdout.getvalue().strip(), '(hbnb)')

    def test_precmd_with_command(self):
        """Test precmd with a valid command input."""
        console = HBNBCommand()
        line = "BaseModel.show('1234')"
        expected = "show BaseModel '1234' "
        self.assertEqual(console.precmd(line), expected)

    def test_precmd_with_invalid_command(self):
        """Test precmd with an invalid command."""
        console = HBNBCommand()
        line = "BaseModel.invalid_command('1234')"
        self.assertEqual(console.precmd(line), line)

    def test_precmd_no_args(self):
        """Test precmd with no arguments."""
        console = HBNBCommand()
        line = "BaseModel.all()"
        expected = "all BaseModel  "
        self.assertEqual(console.precmd(line), expected)

    def test_do_quit(self):
        """Test the quit command exits the program."""
        with self.assertRaises(SystemExit):
            HBNBCommand().do_quit("")

    def test_do_EOF(self):
        """Test the EOF command exits the program."""
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            with self.assertRaises(SystemExit):
                HBNBCommand().do_EOF("")
            self.assertEqual(mock_stdout.getvalue().strip(), '')

    def test_emptyline(self):
        """Test that an empty line does nothing."""
        console = HBNBCommand()
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            console.emptyline()
            self.assertEqual(mock_stdout.getvalue(), "")

    def setUp(self):
        """Clear storage before each test"""
        storage._FileStorage__objects = {}

    def test_create_with_params(self):
        """Test creating an object with parameters"""
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            command = HBNBCommand()
            with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                command.onecmd('create State name="California"')
                state_id = mock_stdout.getvalue().strip()
                self.assertIn("State." + state_id, storage.all())

                state = storage.all()["State." + state_id]
                self.assertEqual(state.name, "California")

    def test_create_with_multiple_params(self):
        """Test creating an object with multiple parameters"""
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            command = HBNBCommand()
            with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                command.onecmd('create Place city_id="0001" user_id="0001" '
                               'name="My_little_house" number_rooms=4 '
                               'number_bathrooms=2 max_guest=10 '
                               'price_by_night=300 latitude=37.773972 '
                               'longitude=-122.431297')
                place_id = mock_stdout.getvalue().strip()
                self.assertIn("Place." + place_id, storage.all())

                place = storage.all()["Place." + place_id]
                self.assertEqual(place.city_id, "0001")
                self.assertEqual(place.user_id, "0001")
                self.assertEqual(place.name, "My little house")
                self.assertEqual(place.number_rooms, 4)
                self.assertEqual(place.number_bathrooms, 2)
                self.assertEqual(place.max_guest, 10)
                self.assertEqual(place.price_by_night, 300)
                self.assertAlmostEqual(place.latitude, 37.773972)
                self.assertAlmostEqual(place.longitude, -122.431297)


if __name__ == "__main__":
    unittest.main()
