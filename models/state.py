#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
# from models.city import City
import os


class State(BaseModel, Base):
    """ State class """
    # __tablename__ = "states"
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship(
                'City', back_populates='state',
                cascade='all, delete, delete-orphan')
    else:
        name = ""

        @property
        def cities(self):
            """Getter attribute cities that returns the list of City instances
            if state_id == current State.id for FileStorage
            """
            from models.city import City
            import models
            my_list = []
            for city_skk in models.storage.all(City).values():
                if city_skk.state_id == self.id:
                    my_list.append(city_skk)
            return my_list

    def __init__(self, *args, **kwargs):
        """initialize"""
        super().__init__(*args, **kwargs)
