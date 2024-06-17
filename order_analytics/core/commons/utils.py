"""
This module provides a simple utils class that can be used to define the common functions
"""
import sqlite3
from pathlib import Path

class Utils:
    """
    A class for managing the utility functions

    """

    def __init__(self,logger,db):
        """
        Initializes the utils class object
        """
        self.logger = logger
        self.db = db
        logger.info("Message from Utils Init")


    def __str__(self) -> str:
        """
        Returns a string representation of the Utils object.

        Returns:
            str: A string representation of the Utils object.
        """
        return "Custom message from Utils STR"
