import json
from json import JSONDecodeError

from flask import Flask, Response, request
from utils.console_logger import get_console_logger

MIN_LINES_TO_SHOW_END = 2


class RequestsDebugger:
    """
    Middleware for logging incoming and outgoing HTTP request payloads.

    This class provides methods to log formatted incoming and outgoing JSON payloads
    with limits on string length and line count to a console logger.

    It integrates with a Flask application to log request details before and after processing.

    Attributes
    ----------
    request_console_logger : logging.Logger
        Console logger instance initialized with "request" as the logging context.
    """

    def __init__(self):
        """
        Initialize a RequestsDebugger instance with a console logger for "request" context.
        """
        self.request_console_logger = get_console_logger('request')

    def init_app(self, app: Flask):
        """
        Initialize the RequestsDebugger middleware with a Flask application instance.

        Sets up before_request and after_request hooks to log incoming and outgoing
        JSON payloads, respectively, to the console logger.

        Parameters
        ----------
        app : Flask
            The Flask application instance to initialize with request logging middleware.
        """

        def _format_str_limit_length(s: str, max_length: int):
            if len(s) > max_length:
                return s[:max_length] + '...'
            else:
                return s

        def _format_multiline_str_limit_lines(lines: [str], max_lines: int):
            if len(lines) > max_lines > MIN_LINES_TO_SHOW_END:
                return [*lines[: max_lines - MIN_LINES_TO_SHOW_END], '...', lines[-2], lines[-1]]
            else:
                return lines

        def _format_multiline_str_limit_both(s: str, max_col_length: int, max_lines: int):
            return '\n'.join(
                _format_str_limit_length(line, max_col_length) for line in _format_multiline_str_limit_lines(s.splitlines(), max_lines)
            )

        @app.before_request
        def log_request_info():
            self.request_console_logger.debug('Incoming payload:')
            if request.data is None or len(request.data) == 0:
                self.request_console_logger.debug('No payload')
            else:
                try:
                    data = json.loads(request.data)
                    message = json.dumps(data, indent=4)
                    self.request_console_logger.debug(_format_multiline_str_limit_both(message, 120, 10))
                except JSONDecodeError:
                    self.request_console_logger.debug('* Not a JSON *')

        @app.after_request
        def after_request(response: Response):
            if response.json is None:
                return response
            message = json.dumps(response.json, indent=4)
            self.request_console_logger.debug('Outgoing payload :')
            self.request_console_logger.debug(_format_multiline_str_limit_both(message, 120, 10))
            return response
