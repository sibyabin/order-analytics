"""
This module provides a simple Logger class that can be used to create
and manage loggers across multiple modules
"""

import logging


class Logger:
    """
    A simple logger class for creating and using loggers across multiple modules.

    Attributes:
        name (str): The name of the logger.
        logger (logging.Logger): The logger instance.
    """

    def __init__(self, name: str):
        """
        Initializes the Logger object with the given name.

        Args:
            name (str): The name of the logger.
        """
        self.name: str = name
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Set the default logging level

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add ch to logger
        self.logger.addHandler(ch)


    def __str__(self) -> str:
        """
        Returns a string representation of the Logger.

        Returns:
            str: A string representation of the Logger.
        """
        return "Custom message from Logger STR"

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        return self.logger
