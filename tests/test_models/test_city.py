#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            new = self.value()
            self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            new = self.value()
            self.assertEqual(type(new.name), str)
