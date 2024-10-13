from errors import BaseCustomError


class EntityNotFoundError(BaseCustomError):
    """
    Exception raised when an entity is not found in the database.

    The EntityNotFoundError class is used to signal that a specific entity
    was not found in the database based on the given search criteria.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, including the model and search criteria that failed.
    """

    def __init__(self, model, **kwargs):
        r"""
        Initialize the EntityNotFoundError instance with the model and search criteria.

        The error message is constructed to include the name of the table and
        the search criteria that did not return any results.

        Parameters
        ----------
        model : class
            The database model class where the search was performed.
        \**kwargs : dict
            The search criteria that were used to find the entity.
        """
        search_that_failed = ', '.join(f'{criterion}={value}' for criterion, value in kwargs.items())
        message = f"No element found on table '{model.__table__}' " f'with the following parameters: {search_that_failed}'
        super().__init__(message)


class MultipleResultsFoundError(BaseCustomError):
    """
    Exception raised when multiple entities are found in the database when only one was expected.

    The MultipleResultsFoundError class is used to signal that a query expecting a single
    result returned multiple entities.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, including the model and search criteria that led to multiple results.
    """

    def __init__(self, model, **kwargs):
        r"""
        Initialize the MultipleResultsFoundError instance with the model and search criteria.

        The error message is constructed to include the name of the table and
        the search criteria that returned multiple results.

        Parameters
        ----------
        model : class
            The database model class where the search was performed.
        \**kwargs : dict
            The search criteria that were used and resulted in multiple entities being found.
        """
        search_that_failed = ', '.join(f'{criterion}={value}' for criterion, value in kwargs.items())
        message = (
            f"Request for one and only one element on table '{model.__table__}', "
            f'but multiple results found with the following parameters: {search_that_failed}'
        )
        super().__init__(message)


class UnknownColumnError(BaseCustomError):
    """
    Exception raised when a specified column is not found in the database table.

    The UnknownColumnError class is used to signal that a specified column does
    not exist in the given database table.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, including the model and the non-existent column name.
    """

    def __init__(self, model, col_name: str):
        """
        Initialize the UnknownColumnError instance with the model and column name.

        The error message is constructed to include the name of the table and
        the column that was not found.

        Parameters
        ----------
        model : class
            The database model class where the column was expected.
        col_name : str
            The name of the column that does not exist in the table.
        """
        message = f"Column '{col_name}' doesn't exist on table '{model.__table__}'"
        super().__init__(message)
