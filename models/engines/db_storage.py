#!/usr/bin/env python3
"""Defines the DBStorage engine."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
from models.users_record_update import User
from sqlalchemy import and_

Base = declarative_base()



class DBStorage:
    """Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
        __classes (dict): Codex of class-names-to-model-types.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("IMS_MYSQL_USER"),
                                             getenv("IMS_MYSQL_PWD"),
                                             getenv("IMS_MYSQL_HOST"),
                                             getenv("IMS_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("IMS_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def get_user(self, email=None, password=None):
        """Retrieve a user from the database by email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The matching User object if found, None otherwise.
        """
        user = self.__session.query(User).filter(and_(User.email == email, User.password == password)).first()
        
        if user:
            return user
        
        return None

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
