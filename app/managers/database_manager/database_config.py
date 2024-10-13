import enum
import os
from urllib.parse import urlparse

from config import config


class DatabaseDialectEnum(enum.Enum):
    """
    Enum representing supported database dialects.

    This enum defines supported database dialects for different types of databases.

    Attributes
    ----------
    POSTGRESQL : DatabaseDialectEnum
        Represents the PostgreSQL database dialect.
    MONGODB : DatabaseDialectEnum
        Represents the MongoDB database dialect.
    """

    POSTGRESQL = 0
    MONGODB = 1

    @staticmethod
    def to_string(dialect: 'DatabaseDialectEnum') -> str:
        """
        Convert a DatabaseDialectEnum value to its corresponding string representation.

        Parameters
        ----------
        dialect : DatabaseDialectEnum
            The database dialect enum value to convert.

        Returns
        -------
        str:
            The string representation of the given database dialect enum value.

        Raises
        ------
        Exception:
            Raised if an invalid database dialect enum value is provided.
        """
        match dialect:
            case DatabaseDialectEnum.POSTGRESQL:
                return 'postgresql'
            case DatabaseDialectEnum.MONGODB:
                return 'mongodb'
            case _:
                raise Exception('Invalid dialect')


class DatabaseConfig:
    """
    Configuration class for handling database connection details.

    The DatabaseConfig class provides methods to initialize database connection details
    either from a database URI, environment variables, or a local URI.

    It also provides engine options based on the database dialect.

    Attributes
    ----------
    db_uri : str
        The database URI used to initialize the configuration.

    dialect : str
        The database dialect extracted from the db_uri.

    db_name : str
        The name of the database extracted from the db_uri.

    db_user : str
        The database username extracted from the db_uri.

    db_pass : str
        The database password extracted from the db_uri.

    db_ip : str
        The IP address or hostname of the database server extracted from the db_uri.

    db_port : int
        The port number of the database server extracted from the db_uri.
    """

    def __init__(self, db_uri: str):
        """
        Initialize DatabaseConfig with details parsed from a database URI.

        Parameters
        ----------
        db_uri : str
            The database URI used to initialize the configuration.
        """
        self.db_uri = db_uri
        parsed_uri = urlparse(db_uri)
        self.dialect = parsed_uri.scheme
        self.db_name = parsed_uri.path
        self.db_user = parsed_uri.username
        self.db_pass = parsed_uri.password
        self.db_ip = parsed_uri.hostname
        self.db_port = parsed_uri.port

    @classmethod
    def from_env_var_prefix(cls, dialect: DatabaseDialectEnum, env_var_prefix: str):
        """
        Initialize DatabaseConfig using environment variables based on a prefix.

        Parameters
        ----------
        dialect : DatabaseDialectEnum
            The database dialect enum specifying the type of database.
        env_var_prefix : str
            The prefix for environment variables containing database connection details.

        Returns
        -------
        DatabaseConfig
            An instance of DatabaseConfig initialized from environment variables.

        Raises
        ------
        Exception
            If any required environment variables are missing.
        """
        missing_env_vars = []

        def _get_env(env_var_name: str) -> str:
            value = os.getenv(env_var_name)
            if value is None:
                missing_env_vars.append(env_var_name)
            return value

        dialect_str = DatabaseDialectEnum.to_string(dialect)
        db_name = _get_env(f'{env_var_prefix}_NAME')
        db_user = _get_env(f'{env_var_prefix}_USER')
        db_pass = _get_env(f'{env_var_prefix}_PASS')
        db_ip = _get_env(f'{env_var_prefix}_IP')
        db_port = _get_env(f'{env_var_prefix}_PORT')

        if len(missing_env_vars) > 0:
            raise Exception(f"Missing environment variables: {', '.join(missing_env_vars)}")
        match dialect:
            case DatabaseDialectEnum.POSTGRESQL:
                return cls(f'{dialect_str}://{db_user}:{db_pass}@{db_ip}:{db_port}/{db_name}')
            case DatabaseDialectEnum.MONGODB:
                if config.ENV != 'deployed':
                    return cls(f'{dialect_str}://{db_user}:{db_pass}@{db_ip}:{db_port}/{db_name}?authSource=admin')
                else:
                    return cls(f'{dialect_str}://{db_user}:{db_pass}@{db_ip}:{db_port}/{db_name}?authSource={db_name}')

    @classmethod
    def from_local_uri(cls, dialect: DatabaseDialectEnum, uri: str):
        """
        Initialize DatabaseConfig using a local URI.

        Parameters
        ----------
        dialect : DatabaseDialectEnum
            The database dialect enum specifying the type of database.
        uri : str
            The local URI containing database connection details.

        Returns
        -------
        DatabaseConfig
            An instance of DatabaseConfig initialized from the local URI.
        """
        dialect_str = DatabaseDialectEnum.to_string(dialect)
        return cls(f'{dialect_str}://{uri}')

    @property
    def engine_options(self) -> dict:
        """
        Get engine options specific to the database dialect.

        Returns
        -------
        dict
            Engine options specific to the database dialect, such as connection pooling settings.

        Notes
        ------
        - Returns an empty dictionary if the database dialect is not recognized or supported.
        """
        if self.dialect == 'postgresql':
            return {
                'pool_pre_ping': True,
                'pool_recycle': 1800,
                'pool_size': 10,
                'max_overflow': 20,
            }
        else:
            return {}
