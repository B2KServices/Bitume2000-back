import logging

from .color_formatter import ColoredFormatter


def setup_console_loggers_color():
    """
    Configures console logging with colored output using a custom ColoredFormatter.

    This function sets up colored logging for the root logger. It initializes logging to
    the console with a format that includes the name of the logger and the log message.
    The log levels are displayed in color using ANSI escape codes for better readability.

    Notes
    -----
    - The function assumes that the `ColoredFormatter` class is defined and imported
      in the current module or package.
    - It modifies the existing handlers of the root logger to use `ColoredFormatter`.

    """
    logging.basicConfig(level=logging.DEBUG, format='[%(name)s] %(message)s', handlers=[logging.StreamHandler()])
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        colored_formatter = ColoredFormatter(handler.formatter._fmt)
        handler.setFormatter(colored_formatter)


def get_console_logger(name):
    """
    Retrieve or create a logger configured for console output with the specified name.

    Parameters
    ----------
    name : str
        The name of the logger to retrieve or create.

    Returns
    -------
    logging.Logger
        A logging.Logger instance configured to output logs to the console with the
        specified name.

    Notes
    -----
    - The function creates a new logger if a logger with the specified name doesn't exist.
    - Logging configuration, such as log level and formatting, may need additional setup
      depending on application requirements.

    """
    return logging.getLogger(name)
