import unittest
from models.engine import db_storage
from models.base_model import BaseModel, Base
from models.state import State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.city import City
import os
DBStorage = db_storage.DBStorage


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


if __name__ == "__main__":
    unittest.main()
