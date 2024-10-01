import logging


class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that adds color to log messages based on log levels.

    This formatter uses ANSI escape codes to colorize log levels for better readability
    in the console.

    It supports the following log levels:

    - DEBUG: Violet color

    - INFO: Green color

    - WARNING: Yellow color

    - ERROR: Red color

    - CRITICAL: White text on red background

    Attributes
    ----------
    COLORS : dict
        A dictionary mapping log level names to ANSI escape codes for coloring.
    """

    COLORS = {
        'RESET': '\033[0m',
        'DEBUG': '\033[1;35m',  # violet
        'INFO': '\033[1;32m',  # vert
        'WARNING': '\033[1;33m',  # jaune
        'ERROR': '\033[1;31m',  # rouge
        'CRITICAL': '\033[1;41m\033[1;37m',  # texte blanc sur fond rouge
    }

    def format(self, record):
        """
        Format the log message with color based on the log level.

        Parameters
        -----------
        record : logging.LogRecord
            The LogRecord object containing log information.

        Returns
        -------
        str:
            Formatted log message with ANSI escape codes for color.
        """
        log_message = super().format(record)
        log_level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        return '\n'.join(f"{log_level_color}{line}{self.COLORS['RESET']}" for line in log_message.splitlines())
