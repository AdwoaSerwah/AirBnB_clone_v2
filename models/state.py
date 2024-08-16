#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import os
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
                'City', backref='state', cascade='all, delete, delete-orphan')
    else:
        @property
        def cities(self):
            """Getter attribute cities that returns the list of City instances
            if state_id == current State.id for FileStorage
            """
            my_list = []
            for city_skk in models.storage.all(City).values():
                if city_skk.state_id == self.id:
                    my_list.append(city_skk)
            return my_list
