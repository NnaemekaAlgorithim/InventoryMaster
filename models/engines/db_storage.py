#!/usr/bin/env python3
"""Defines the DBStorage engine."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
from models.users import User
from models.inventory import Inventory
from models.sales import Sales
from sqlalchemy import and_
from sqlalchemy import text, column, select

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
    __classes = {
        "User": User,
        "Inventory": Inventory,
        "Sales": Sales
    }

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

    def delete_user(self, user_id, class_name):
        """Delete all data for a given user_id from the current database session."""
        objects_to_delete = self.__session.query(class_name).filter_by(user_id=user_id).all()
    
        for obj in objects_to_delete:
            self.__session.delete(obj)
        self.__session.commit()

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

    def get_inventory(self, user_id=None, name_of_product=None):
        """Retrieve an inventory item from the database by user_id and product_name.

        Args:
            user_id (int): The user's ID.
            product_name (str): The name of the product.

        Returns:
            Inventory: The matching Inventory object if found, None otherwise.
        """

        inventory = self.__session.query(Inventory).filter(and_(Inventory.user_id == user_id, Inventory.product_name == name_of_product)).first()

        if inventory:
            return inventory

        return None

    def get_all(self, user_id, class_name):
        """Retrieve objects from the specified table by user_id.

        Args:
            user_id (int): The user's ID.
            class_name (str): The name of the class representing the database table.

        Returns:
            list: A list of matching objects if found, an empty list otherwise.
        """

        # Query the table based on the user_id
        objects = []
        objects = self.__session.query(class_name).filter(class_name.user_id == user_id).all()
        if not objects:
            return []

        return objects
    
    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
