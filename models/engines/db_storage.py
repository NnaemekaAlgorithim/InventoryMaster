#!/usr/bin/env python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base, BaseModel
from models.users_record_update import Users
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker


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
        "Users": Users,
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

    def all(self, cls, user_id):
        """Query on the current database session all objects of the given class and user_id.

        Args:
            cls (str): The class name to query.
            user_id (int): The user ID to filter the results.

        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if type(cls) == str:
            cls = eval(cls)
        objs = self.__session.query(cls).filter_by(user_id=user_id).all()
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

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

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()

    def get(self, cls, id, user_id):
        """Returns a given instance from __objects.

        Args:
            cls (str): The class name of the instance to retrieve.
            id (str): The ID of the instance to retrieve.
            user_id (int): The user ID to filter the results.

        Returns:
            The requested instance or None if not found.
        """
        try:
            obj = eval(cls)
        except NameError:
            return None
        if obj in self.__classes.values():
            return self.__session.query(obj).filter_by(user_id=user_id, id=id).first()

    def count(self, cls, user_id):
        """Returns a count of all instances of the given class in __objects.

        Args:
            cls (str): The class type to count instances of.
            user_id (int): The user ID to filter the results.

        Returns:
            The count of instances.
        """
        if type(cls) == str and cls in self.__classes.keys():
            count = self.__session.query(self.__classes[cls]).filter_by(user_id=user_id).count()
            return count
        return

    def register_user(self, user_data):
        """Register a new user and create a corresponding user object.

        Args:
            user_data (dict): User data containing username, password, etc.

        Returns:
            The newly created user object.
        """
        user = Users(**user_data)
        self.new(user)
        self.save()
        return user

    def login_user(self, username, password):
        """Authenticate a user by username and password.

        Args:
            username (str): The username.
            password (str): The password.

        Returns:
            The user object if the authentication is successful, None otherwise.
        """
        user = self.__session.query(Users).filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
