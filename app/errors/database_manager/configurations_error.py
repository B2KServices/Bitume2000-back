from errors import BaseCustomError


class MissingEnvironnmentVariablesError(BaseCustomError):
    def __init__(self, missing_env_vars: list[str]):
        super().__init__(f"Missing environment variables: {', '.join(missing_env_vars)})")


class InvalidDialectError(BaseCustomError):
    def __init__(self, dialect: str, supported_dialects: list[str]):
        super().__init__(f"Unrecognized database dialect: {dialect}, supported dialects are: {', '.join(supported_dialects)}")


class PostgresAlreadyDefineError(BaseCustomError):
    """
    Raise an error when attempting to define a PostgreSQL database that is already defined.

    Inherits
    --------
    FlaskDatabaseError : class
        Base class for exceptions related to Flask database errors.
    """

    def __init__(self):
        """Initialize the PostgresAlreadyDefineError with a default message."""
        super().__init__('Postgres is already defined')
