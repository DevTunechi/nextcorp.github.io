#!/usr/bin/env python3

import models
import sqlalchemy
from models.base_model import BaseModel, Base
from models.corp import Corp
from models.employee import Employee
from models.checker import CheckInOut
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError


classes = {"Corp": Corp, "Employee": Employee,
           "CheckInOut": CheckInOut}

class DBStorage:
    """ Interacts with the MySQL database """
    __engine = None
    __session = None

    def __init__(self):
        """ Instantiate a DBStorage obj """
        NC_MYSQL_USR = getenv('NC_MYSQL_USR')
        NC_MYSQL_PWD = getenv('NC_MYSQL_PWD')
        NC_MYSQL_HOST = getenv('NC_MYSQL_HOST')
        NC_MYSQL_PORT = getenv('NC_MYSQL_PORT')
        NC_MYSQL_DB = getenv('NC_MYSQL_DB')
        NC_ENV = getenv('NC_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.
                                      format(NC_MYSQL_USR,
                                             NC_MYSQL_PWD,
                                             NC_MYSQL_HOST,
                                             NC_MYSQL_PORT,
                                             NC_MYSQL_DB))

        if NC_ENV == "drop":
            Base.metadata.drop_all(self.__engine)

        # Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # self.__session = Session()


    def new(self, obj):
        """ Add the object to the current db session """
        self.__session.add(obj)

    def save(self):
        """ Commits all challenges of the current database session """
        # self.__session.commit()
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            self.rollback()
            raise

    def delete(self, obj=None):
        """ Delete obj from the current database session """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Crates all tables in the database and create the session """
        Base.metadata.create_all(self.__engine)
        """
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()
        """
        self.__session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(self.__session_factory)

    def all(self, cls=None):
        """ Query on the current database session """
        result = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    result[key] = obj
        return result

    """
    def get(self, cls, id):
        # Retrieves a single object
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for v in all_cls.values():
            if (v.id == id):
                return v

        return None
    """
    def get(self, cls, id):
        """ Retrieves a single obj """
        if isinstance(cls, str):
            cls = classes.get(cls)
        if cls not in classes.values():
            return None

        return self.__session.query(cls).get(id)

    def count(self, cls=None):
        """ Counts the num of objects in storage """
        all_class = classes.values()
        if not cls:
            count = 0
            for c in all_class:
                count += len(models.storage.all(c).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def rollback(self):
        """ Rollback Database Record """
        if self.__session:
            self.__session.rollback()

    def close(self):
        """ Close the current database session """
        # self.__session.close()
        if self.__session:
            self.__session.close()
