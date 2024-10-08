#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

        state = relationship('State', back_populates='cities')
        places = relationship(
                'Place', back_populates='cities',
                cascade='all, delete, delete-orphan')
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """Create city instance"""
        super().__init__(*args, **kwargs)
