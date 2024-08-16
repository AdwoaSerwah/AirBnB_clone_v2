#!/usr/bin/python3
""" Console Module """
import cmd
import sys
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
    def test_prompt(self):
        """Test that the prompt is correct in interactive mode."""
        with patch('sys.__stdin__.isatty', return_value=True):
            console = HBNBCommand()
            self.assertEqual(console.prompt, '(hbnb) ')

    def test_prompt_non_interactive(self):
        """Test that the prompt is correct in non-interactive mode."""
        with patch('sys.__stdin__.isatty', return_value=False):
            console = HBNBCommand()
            self.assertEqual(console.prompt, '(hbnb) ')

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


if __name__ == "__main__":
    unittest.main()
