import unittest
import MySQLdb
from io import StringIO
from console import HBNBCommand
import unittest
from models.base_model import BaseModel
from models import storage
import os
import sys

class TestConsoleMySQL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up MySQL connection and initial test conditions"""
        cls.db = MySQLdb.connect(
            host="localhost",
            user="hbnb_test",         # Replace with your MySQL username
            passwd="hbnb_test_pwd",   # Replace with your MySQL password
            db="hbnb_test_db"        # Replace with your test database name
        )
        cls.cursor = cls.db.cursor()

    @classmethod
    def tearDownClass(cls):
        """Clean up and close MySQL connection"""
        cls.cursor.close()
        cls.db.close()

    def test_create_state(self):
        """Test the `create State name="California"` command"""

        # Get the number of records before running the command
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Execute the console command
        sys.stdout = StringIO()  # Redirect stdout to capture console output
        HBNBCommand().onecmd('create State name="California"')
        sys.stdout = sys.__stdout__  # Reset stdout

        # Get the number of records after running the command
        self.cursor.execute("SELECT COUNT(*) FROM states")
        new_count = self.cursor.fetchone()[0]

        # Check if the record count has increased by 1
        self.assertEqual(new_count, initial_count + 1)

if __name__ == '__main__':
    unittest.main()
