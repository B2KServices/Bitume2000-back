import os
from typing import Final

from dotenv import load_dotenv


class BaseConfig:
    """
    Configuration class for setting up base environment variables and API specifications.

    Attributes
    ----------
    MIGRATION : str
        Migration environment variable for database migrations.
    KEYCLOAK_URL : str
        Keycloak server URL for authentication and authorization.
    KEYCLOAK_REALM : str
        Keycloak realm name for authentication and authorization.
    KEYCLOAK_CLIENT_ID : str
        Keycloak client ID for client authentication.
    KEYCLOAK_CLIENT_SECRET : str
        Keycloak client secret for client authentication.
    KEYCLOAK_GROUP : str or None
        Optional Keycloak group name for user authorization.
    KEYCLOAK_CLIENT_ID : str
        Keycloak authentication client for user authentication.
    APISPEC_SPEC : APISpec
        APISpec object defining API documentation specifications.
    APISPEC_SWAGGER_UI_URL : str
        URL path for accessing the Swagger UI documentation.

    Notes
    -----
    - Initializes environment variables using `os.getenv`.
    - Configures `APISPEC_SPEC` with API documentation settings including title, version, security definitions,
      and Swagger UI configuration.
    """

    def __init__(self):
        # Flask
        self.MIGRATION: Final[str] = os.getenv('MIGRATION')
        self.JWT_SECRET_KEY: Final[str] = os.getenv('JWT_SECRET_KEY')
        self.JWT_TOKEN_LOCATION: Final[list[str]] = ['cookies', 'headers']
        self.JWT_ACCESS_COOKIE_PATH: Final[str] = '/api/'
        self.JWT_REFRESH_COOKIE_PATH: Final[str] = '/token/refresh'
        self.JWT_COOKIE_CSRF_PROTECT: Final[bool] = False
        self.DISCORD_BOT_TOKEN: Final[str] = os.getenv('DISCORD_BOT_TOKEN')
        self.GUILD_ID: Final[str] = os.getenv('GUILD_ID')
        self.ANNOUNCEMENT_CHANNEL_ID: Final[str] = os.getenv('ANNOUNCEMENT_CHANNEL_ID')


class TestingConfig(BaseConfig):
    """
    Configuration class for testing environment.

    This class inherits from BaseConfig and sets specific configurations
    for testing purposes.

    Attributes
    ----------
    DEBUG : bool
        Flag indicating whether debug mode is enabled.
    ENV : str
        Environment name, set to "test" for testing environment.

    Notes
    -----
    - Inherits configurations from BaseConfig.
    - DEBUG is set to True to enable debug mode in the testing environment.
    - ENV is set to "test" to indicate the environment type as testing.
    """

    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = 'test'


class DevelopmentConfig(BaseConfig):
    """
    Configuration class for development environment.

    This class inherits from BaseConfig and sets specific configurations
    for development purposes.

    Attributes
    ----------
    DEBUG : bool
        Flag indicating whether debug mode is enabled.
    ENV : str
        Environment name, set to "dev" for development environment.

    Notes
    -----
    - Inherits configurations from BaseConfig.
    - DEBUG is set to True to enable debug mode in the development environment.
    - ENV is set to "dev" to indicate the environment type as development.
    """

    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = 'local'


class ProductionConfig(BaseConfig):
    """
    Configuration class for production environment.

    This class inherits from BaseConfig and sets specific configurations
    for production purposes.

    Attributes
    ----------
    DEBUG : bool
        Flag indicating whether debug mode is enabled. Set to False for production.
    ENV : str
        Environment name, set to "prod" for production environment.

    Notes
    -----
    - Inherits configurations from BaseConfig.
    - DEBUG is set to False to disable debug mode in the production environment.
    - ENV is set to "prod" to indicate the environment type as production.
    """

    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.ENV = 'deployed'


def load_config():
    """
    Load configuration settings based on the environment variable `ENV`.

    Returns
    -------
    BaseConfig
        Configuration settings based on the environment variable `ENV`.

    Raises
    ------
    Exception
        If the environment variable `ENV` is not set to a valid value.
    """
    load_dotenv()
    match os.getenv('ENV'):
        case 'test':
            return TestingConfig()
        case 'deployed':
            return ProductionConfig()
        case 'local' | '' | None:
            return DevelopmentConfig()
        case _:
            raise Exception(
                f"Incorrect value for environment variable ENV: '{os.getenv('ENV')}'. " f"Possible values: test, local, deployed  (default: local)"
            )


config = load_config()
