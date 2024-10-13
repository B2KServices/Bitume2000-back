import sys

from errors.database_manager.configurations_error import PostgresAlreadyDefineError
from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from managers.database_manager.database_config import (
    DatabaseConfig,
    DatabaseDialectEnum,
)
from utils.console_logger import get_console_logger

database_manager_logger = get_console_logger('database_manager')


class DatabaseManager:
    """
    Manager class for handling PostgreSQL and MongoDB databases.

    The DatabaseManager class provides methods to add PostgreSQL and MongoDB databases,
    initialize them based on environment variables or local URIs, and configure them
    for a Flask application.

    Attributes
    ----------
    postgres_database : dict or None
        Dictionary containing SQLAlchemy database instance and environment variable prefix
        for PostgreSQL database configuration. None if not initialized.

    mongo_databases : list
        List of dictionaries, each containing environment variable prefix and PyMongo
        database instance for MongoDB configurations.

    Notes
    -----
    - Supports only one PostgreSQL database instance due to limitation.
    - Initializes MongoDB connections and logs connection status.
    """

    def __init__(self):
        """
        Initialize an instance of DatabaseManager with empty lists for databases.
        """
        self.postgres_database = None
        self.mongo_databases = []

    def add_postgres_database(self, env_var_prefix: str) -> SQLAlchemy:
        """
        Add a PostgreSQL database instance to the manager.

        Parameters
        ----------
        env_var_prefix : str
            Prefix for environment variables containing PostgreSQL database details.

        Returns
        -------
        SQLAlchemy
            SQLAlchemy database instance initialized for PostgreSQL.

        Raises
        ------
        Exception
            If a PostgreSQL database instance is already added.
        """
        if self.postgres_database is not None:
            raise PostgresAlreadyDefineError()
        db = SQLAlchemy()
        self.postgres_database = {'db': db, 'env_var_prefix': env_var_prefix}
        return db

    def add_mongo_database(self, env_var_prefix: str) -> PyMongo:
        """
        Add a MongoDB database instance to the manager.

        Parameters
        ----------
        env_var_prefix : str
            Prefix for environment variables containing MongoDB database details.

        Returns
        -------
        MongoClient
            PyMongo database instance initialized for MongoDB.
        """
        mongo = PyMongo()
        self.mongo_databases.append({'env_var_prefix': env_var_prefix, 'mongo': mongo})
        return mongo

    def init_app(self, app: Flask):
        """
        Initialize databases for the Flask application based on environment settings.

        Parameters
        ----------
        app : Flask
            The Flask application instance to configure with database settings.

        Notes
        -----
        - Initializes PostgreSQL and MongoDB databases based on environment variables or local URIs.
        - Logs connection status for MongoDB databases.
        """
        if self.postgres_database is not None:
            db_data = self.postgres_database
            env_var_prefix = db_data['env_var_prefix']
            db_config = DatabaseConfig.from_env_var_prefix(DatabaseDialectEnum.POSTGRESQL, env_var_prefix)
            app.config['SQLALCHEMY_DATABASE_URI'] = db_config.db_uri
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = db_config.engine_options
            db_data['db'].init_app(app)
        for db_data in self.mongo_databases:
            env_var_prefix = db_data['env_var_prefix']
            db_config = DatabaseConfig.from_env_var_prefix(DatabaseDialectEnum.MONGODB, env_var_prefix)
            db_data['mongo'].init_app(app, uri=db_config.db_uri)
            try:
                db_data['mongo'].cx.server_info()
                app.logger.info('Successfully connected to MongoDB')
            except Exception as e:
                app.logger.error(f'An error occurred: {e}')
                sys.exit(1)
            database_manager_logger.debug(f'Using database {db_config.db_name} uri: {db_config.db_uri}')
