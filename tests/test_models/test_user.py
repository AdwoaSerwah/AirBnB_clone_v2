#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User
import os
from models.place import Place
from models import storage
from datetime import datetime


class test_User(test_basemodel):
    """ """
    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            new = self.value()
            self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            new = self.value()
            self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            new = self.value()
            self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            new = self.value()
            self.assertEqual(type(new.password), str)

    def test_created_at(self):
        """ Test the created_at attribute """
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            new = self.value()
            self.assertTrue(hasattr(new, 'created_at'))
            self.assertIsInstance(new.created_at, datetime)
            self.assertEqual(type(new.created_at), datetime)
