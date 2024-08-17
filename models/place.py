#!/usr/bin/python3
"""This module defines a class Place"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
# from models.review import Review
import os
import models


class Place(BaseModel, Base):
    """This class defines a place class"""
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    """if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
                'Review', backref='place', cascade='all, delete, delete-orphan')
    else:
        @property
        def reviews(self):
            Getter attribute reviews returns the list of Review instances
            if place_id == current Place.id for FileStorage
            
            my_list = []
            for review_skk in models.storage.all(Review).values():
                if review_skk.place_id == self.id:
                    my_list.append(review_skk)
            return my_list"""
