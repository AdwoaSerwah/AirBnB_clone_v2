#!/usr/bin/python3
"""This module defines a class Amenity"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class Amenity(BaseModel, Base):
    """This class defines an amenity by various attributes"""
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        from models.place import place_amenity
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)

        place_amenities = relationship(
                'Place',
                secondary=place_amenity,
                back_populates='amenities'
                )
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
