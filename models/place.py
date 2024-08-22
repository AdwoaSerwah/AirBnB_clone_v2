#!/usr/bin/python3
"""This module defines a class Place"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
# from models.review import Review
import os
import models

# Define table for creating many-to-many relationship between Place and Amenity
if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column(
                'place_id', String(60),
                ForeignKey(
                    'places.id', ondelete='CASCADE', onupdate='CASCADE'),
                primary_key=True,
                nullable=False),
            Column(
                'amenity_id',
                String(60),
                ForeignKey(
                    'amenities.id', ondelete='CASCADE', onupdate='CASCADE'),
                primary_key=True,
                nullable=False)
            )


class Place(BaseModel, Base):
    """This class defines a place class"""
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
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

        user = relationship('User', back_populates='places')
        cities = relationship('City', back_populates='places')
        reviews = relationship(
                'Review', back_populates='place',
                cascade='all, delete, delete-orphan')

        amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            viewonly=False,
            back_populates='place_amenities'
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            Getter attribute reviews returns the list of Review instances
            if place_id == current Place.id for FileStorage
            """
            from models.review import Review
            my_list = []
            for review_skk in models.storage.all(Review).values():
                if review_skk.place_id == self.id:
                    my_list.append(review_skk)
            return my_list

        @property
        def amenities(self):
            """Getter for amenities when using FileStorage"""
            from models.amenity import Amenity
            return [
                models.storage.get(Amenity, amenity_id)
                for amenity_id in self.amenity_ids
            ]

        @amenities.setter
        def amenities(self, amenity):
            """Setter for amenities when using FileStorage"""
            from models.amenity import Amenity
            # amenity_ids = []
            if isinstance(amenity, Amenity):
                if amenity.id not in self.amenity_ids:
                    self.amenity_ids.append(amenity.id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amenity_ids = []
