import bcrypt
from errors import BaseCustomError
from errors.authentication_errors import UnauthorizedError
from errors.authentication_errors.wrong_password import WrongPasswordError
from marshmallow_sqlalchemy.schema import SQLAlchemySchemaMeta
from utils.registry import SQLAlchemyRegistry


class PasswordAuthManager:
    """
    Authentication module using passwords.

    This module provides functions for registering user profiles, and authenticating users based on passwords.
    """

    def __init__(self, user_model: type[SQLAlchemySchemaMeta]):
        r"""
        Initialize the PasswordAuthManager with the user model.

        The PasswordAuthManager is initialized with the user model class that
        will be used for user authentication.

        Parameters
        ----------
        user_model : class
            The SQLAlchemy model class that represents user profiles.
        """
        if not hasattr(user_model, 'password') or not hasattr(user_model, 'username'):
            raise ValueError("user_model must have 'password' and 'username' attributes")
        self.user_registry = SQLAlchemyRegistry(user_model)

    def authenticate_user_by_name(self, username, password):
        """
        Authenticate a user by their username and password_authentication.

        :param username: The username for authentication.
        :param password: The user's password_authentication to be checked.

        :raises UserNotFoundException: If there is an issue with retrieving user information.
        """

        try:
            user = self.user_registry.get_one_or_fail_where(username=username)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return user
        except BaseCustomError:
            pass
        raise UnauthorizedError()

    def authenticate_user_by_email(self, email, password):
        """
        Authenticate a user by their email and password_authentication.

        :param email: The email for authentication.
        :param password: The user's password_authentication to be checked.

        :raises UserNotFoundException: If there is an issue with retrieving user information.
        """

        user = self.user_registry.get_one_or_fail_where(email=email)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        raise WrongPasswordError()

    def hash_password(self, password):
        """
        Hash a password_authentication using bcrypt.

        :param password: The password_authentication to be hashed.
        :return: The hashed password_authentication.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
