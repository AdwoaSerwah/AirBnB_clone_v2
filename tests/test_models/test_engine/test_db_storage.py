import unittest
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel, Base
from models.state import State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class TestDBStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(cls.engine)
        cls.session = scoped_session(sessionmaker(bind=cls.engine))
        cls.storage = DBStorage()
        cls.storage._DBStorage__session = cls.session

    @classmethod
    def tearDownClass(cls):
        """Tear down test environment"""
        Base.metadata.drop_all(cls.engine)
        cls.session.remove()
        cls.session.bind.dispose()
        os.remove('test.db')

    def setUp(self):
        """Set up before each test"""
        self.session.begin_nested()

    def tearDown(self):
        """Tear down after each test"""
        self.session.rollback()

    def test_create_state(self):
        """Test creation and saving of State object"""
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()

        result = self.session.query(State).filter_by(name="California").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "California")

    def test_get_object(self):
        """Test retrieving an object by id"""
        state = State(name="New York")
        self.storage.new(state)
        self.storage.save()
        state_id = state.id

        retrieved_state = self.storage.get(State, state_id)
        self.assertEqual(state_id, retrieved_state.id)
        self.assertEqual(state.name, retrieved_state.name)

    def test_delete_object(self):
        """Test deleting an object"""
        state = State(name="Texas")
        self.storage.new(state)
        self.storage.save()
        state_id = state.id

        self.storage.delete(state)
        self.storage.save()

        result = self.session.query(State).filter_by(id=state_id).first()
        self.assertIsNone(result)

    def test_reload(self):
        """Test reloading the database"""
        self.storage.reload()
        states = self.session.query(State).all()
        self.assertGreater(len(states), 0)  # Assuming there are states in the database

if __name__ == '__main__':
    unittest.main()
