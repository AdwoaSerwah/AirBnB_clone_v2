#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os
# from models import storage


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # cls.my_env = os.getenv('HBNB_ENV')
        # if os.getenv('HBNB_ENV') == "db":
        cls.storage = FileStorage()
        if os.getenv('HBNB_ENV') != "db":
            cls.storage.reload()

    def setUp(self):
        """ Set up test environment """
        if os.getenv('HBNB_ENV') != "db":
            del_list = []
            for key in self.storage._FileStorage__objects.keys():
                del_list.append(key)
            for key in del_list:
                del self.storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        if os.getenv('HBNB_ENV') != "db":
            try:
                os.remove('file.json')
            except:
                pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        if os.getenv('HBNB_ENV') != "db":
            self.assertEqual(len(self.storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        if os.getenv('HBNB_ENV') != "db":
            new = BaseModel()
            self.storage.new(new)
            expected_key = f'BaseModel.{new.id}'
            temp = self.storage.all().get(expected_key, None)
            self.assertIs(temp, new)

    def test_all(self):
        """ __objects is properly returned """
        if os.getenv('HBNB_ENV') != "db":
            new = BaseModel()
            temp = self.storage.all()
            self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        if os.getenv('HBNB_ENV') != "db":
            new = BaseModel()
            self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        if os.getenv('HBNB_ENV') != "db":
            new = BaseModel()
            thing = new.to_dict()
            self.storage.save()
            new2 = BaseModel(**thing)
            self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        if os.getenv('HBNB_ENV') != "db":
            new = BaseModel()
            self.storage.save()
            self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        if os.getenv('HBNB_ENV') != "db":
            new = BaseModel()
            self.storage.new(new)
            self.storage.save()
            self.storage.reload()
            new_id = new.id
            loaded = None
            all_objects = self.storage.all()
            for obj in all_objects.values():
                if obj.id == new_id:
                    loaded = obj
                    break
            self.assertIsNotNone(loaded, "No object was loaded from storage")
            self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        if os.getenv('HBNB_ENV') != "db":
            with open('file.json', 'w') as f:
                pass
            with self.assertRaises(ValueError):
                self.storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        if os.getenv('HBNB_ENV') != "db":
            self.assertEqual(self.storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        if os.getenv('HBNB_ENV') != "db":
            new = BaseModel()
            self.storage.save()
            self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        if os.getenv('HBNB_ENV') != "db":
            self.assertEqual(type(self.storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        if os.getenv('HBNB_ENV') != "db":
            self.assertEqual(type(self.storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        if os.getenv('HBNB_ENV') != "db":
            new = BaseModel()
            _id = new.to_dict()['id']
            self.storage.new(new)
            self.storage.save()
            key = f'BaseModel.{_id}'
            self.assertIn(key, self.storage.all().keys())

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        if os.getenv('HBNB_ENV') != "db":
            # from models.engine.file_storage import FileStorage
            print(type(self.storage))
            self.assertEqual(type(self.storage), FileStorage)
