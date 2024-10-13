from flask import Response, jsonify


def _default_response(status: str, *, message: str | None = None) -> Response:
    """
    Generates a default response dictionary with status and optional message.

    Parameters
    ----------
    status : str
        The status of the response, indicating success or failure.
    message : str or None, optional
        Optional message associated with the response. Defaults to None if not provided.

    Returns
    -------
    DefaultResponseType
        A dictionary representing the default response with 'status' and 'message' keys.

    Notes
    -----
    - Used for creating consistent response objects in APIs or services.
    """
    return jsonify({'status': status, 'message': message})


class DefaultResponse:
    """
    Utility class for generating default response objects.
    """

    @staticmethod
    def success(message: str | None = None) -> Response:
        """
        Generates a success response with an optional message.

        Parameters
        ----------
        message : str or None, optional
            Optional message associated with the success response. Defaults to None if not provided.

        Returns
        -------
        DefaultResponseType
            A dictionary representing the success response with 'status' as 'success' and 'message' as provided.

        Notes
        -----
        - Uses `_default_response` function internally to generate the response dictionary.
        """
        return _default_response('success', message=message)

    @staticmethod
    def error(message: str) -> Response:
        """
        Generates an error response with a mandatory message.

        Parameters
        ----------
        message : str
            Mandatory message associated with the error response.

        Returns
        -------
        DefaultResponseType
            A dictionary representing the error response with 'status' as 'error' and 'message' as provided.

        Notes
        -----
        - Uses `_default_response` function internally to generate the response dictionary.
        """
        return _default_response('error', message=message)
