"""
Module for managing application error handlers.

This module defines the `AppErrorHandlers` class, which facilitates the setup of global error
handlers in a Flask application. It also includes utility functions for filtering error messages.

Functions
---------
_filter_error_messages(error_messages: str) -> str
    Extracts and returns a filtered version of error messages, removing unwanted characters.

Classes
-------
AppErrorHandlers : class
    A class that allows for adding custom error handlers to a Flask application.
    It initializes the application with error handling capabilities and provides
    methods to register specific error handlers.

Attributes
----------
flask_error_logger : Logger
    Logger instance for recording error handler events and issues.
"""

import re

from flask import Flask
from utils.console_logger import get_console_logger
from utils.request_default_responses import DefaultResponse

flask_error_logger = get_console_logger('flask_error_handler')


def _filter_error_messages(error_messages):
    """
    Extract the content within square brackets from an error message.

    This function searches for the first occurrence of text enclosed in square brackets
    within the provided error message string. If found, it returns the content within
    the brackets, with any double quotes removed. If no brackets are found, the original
    error message is returned.

    Parameters
    ----------
    error_messages : str
        The error message string to be filtered.

    Returns
    -------
    str
        The filtered error message or the original message if no brackets are found.
    """
    match = re.search(r'\[(.*?)\]', error_messages)
    return match.group(1).replace('"', '') if match else error_messages


class AppErrorHandlers:
    """
    Manage error handlers for a Flask application.

    The `AppErrorHandlers` class provides methods to initialize a Flask application
    with custom error handlers. It ensures that specific exceptions are caught and
    properly logged, returning standardized error responses.

    Attributes
    ----------
    app : Flask or None
        The Flask application instance. Initially set to `None` and assigned during initialization.

    Methods
    -------
    add_error_handler(error_class, status_code)
        Add an error handler for a specific exception class with a given status code.
    init_app(app: Flask)
        Initialize the class with a Flask application instance.
    """

    def __init__(self):
        """
        Initialize the AppErrorHandlers instance.

        This constructor initializes the `app` attribute to `None`.
        The `init_app` method should be called to assign a Flask application instance.
        """
        self.app = None

    def register(self, error_class: type[Exception], status_code: int):
        """
        Register an error handler for the specified exception class.

        This method registers a handler for the given `error_class` in the Flask application.
        When the specified error is raised, it will be logged, and a standardized error response
        with the given `status_code` will be returned.

        Parameters
        ----------
        error_class : Exception
            The exception class to handle.
        status_code : int
            The HTTP status code to return with the error response.

        Raises
        ------
        Exception
            If the `AppErrorHandlers` instance has not been initialized with a Flask app.
        """
        if self.app is None:
            flask_error_logger.error('AppErrorHandlers not initialized')
            raise Exception('AppErrorHandlers not initialized')

        @self.app.errorhandler(error_class)
        def handle_error(error):
            flask_error_logger.error(error)
            return DefaultResponse.error(message=str(error)), status_code

        flask_error_logger.debug(f'Error handler added for {error_class.__name__} with status code {status_code}')

    def init_app(self, app: Flask):
        """
        Initialize the AppErrorHandlers instance with a Flask application.

        This method assigns a Flask application instance to the `app` attribute,
        allowing error handlers to be added via the `add_error_handler` method.

        Parameters
        ----------
        app : Flask
            The Flask application instance to associate with this handler.
        """
        self.app = app
        flask_error_logger.info('AppErrorHandlers initialized')
