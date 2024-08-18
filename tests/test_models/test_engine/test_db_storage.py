import unittest
import os
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel, Base
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class TestDBStorage(unittest.TestCase):
    """Testing DBStorage"""
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.storage = DBStorage()
        cls.storage.reload()

    def test_create_state(self):
        """Test creating a new State instance"""
        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()

        states = self.storage.all(State)
        self.assertIn(f"State.{new_state.id}", states)
        self.assertEqual(states[f"State.{new_state.id}"].name, "California")

    def test_get_state(self):
        """Test retrieving a State instance"""
        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()

        retrieved_state = self.storage.all(State).get(f"State.{new_state.id}")
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.name, "California")

    def test_update_state(self):
        """Test updating a State instance"""
        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()

        # Update the name of the state
        new_state.name = "New California"
        self.storage.save()

        updated_state = self.storage.all(State).get(f"State.{new_state.id}")
        self.assertEqual(updated_state.name, "New California")

    def test_delete_state(self):
        """Test deleting a State instance"""
        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()

        self.storage.delete(new_state)
        self.storage.save()

        deleted_state = self.storage.all(State).get(f"State.{new_state.id}")
        self.assertIsNone(deleted_state)

    def test_count_states(self):
        """Test counting the number of State instances"""
        initial_count = len(self.storage.all(State))

        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()

        final_count = len(self.storage.all(State))
        self.assertEqual(final_count, initial_count + 1)

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary"""
        result = self.storage.all(State)
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
