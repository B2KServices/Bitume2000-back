from errors import BaseCustomError


class GroupUnauthorizedKeycloakError(BaseCustomError):
    """
    Exception raised when a user is unauthorized to access a Keycloak group.

    The GroupUnauthorizedKeycloak class is used to signal that a user does not have
    authorization to access a specific Keycloak group.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, indicating the authorized group name.
    """

    def __init__(self, group_name: str):
        """
        Initialize the GroupUnauthorizedKeycloak instance with the unauthorized group name.

        The error message is constructed to indicate the unauthorized group name.

        Parameters
        ----------
        group_name : str
            The name of the Keycloak group that the user is unauthorized to access.
        """
        super().__init__(f'Unauthorized, authorized group: {group_name}')


class KeycloakUnauthorizedError(BaseCustomError):
    """
    Exception raised for unauthorized access in Keycloak.

    The KeycloakUnauthorizedError class is used to signal that an operation in
    Keycloak was unauthorized or access was denied.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, providing details about the unauthorized access.
    """

    def __init__(self, message: str):
        """
        Initialize the KeycloakUnauthorizedError instance with a custom error message.

        The error message should provide details about the specific condition or
        reason for the unauthorized access in Keycloak.

        Parameters
        ----------
        message : str
            A descriptive message explaining why the unauthorized access occurred.
        """
        super().__init__(message)
