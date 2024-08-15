#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given key-value pair"""
        keys, values = [], []

        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise InvalidRequestError()
            keys.append(getattr(User, k))
            values.append(v)

        user_found = self._session.query(User).filter(
            tuple_(*keys).in_([tuple(values)])
        ).first()

        if user_found is None:
            raise NoResultFound()
        return user_found

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user"""
        user = self.find_user_by(id=user_id)
        if user is None:
            return

        user_update = {}
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise ValueError()
            user_update[getattr(User, k)] = v

        self._session.query(User).filter(User.id == user_id).update(
            user_update, synchronize_session=False,
        )
        self._session.commit()
