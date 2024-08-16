#!/usr/bin/python3
"""DBStorage engine for the HBNB project"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
# from models.user import User
# from models.state import State
#from models.city import City
# from models.amenity import Amenity
# from models.place import Place
# from models.review import Review


class DBStorage:
    """Class representing Database storage engine for MySQL using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Create DBStorage class instance"""
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f"mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}"
            f"@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}",
            pool_pre_ping=True
        )

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query current database session"""
        objs_sk = {}
        if cls:
            data = self.__session.query(cls).all()
            for obj in data:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objs_sk[key] = obj
        else:
            fields_sk = [User, State, City, Amenity, Place, Review]
            for cls in fields_sk:
                data = self.__session.query(cls).all()
                for obj in data:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objs_sk[key] = obj
        return objs_sk

    def new(self, obj):
        """Add new object to the current database"""
        self.__session.add(obj)

    def save(self):
        """Save all changes made to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the db and create session"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        ses_f = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(ses_f)
        self.__session = Session()
