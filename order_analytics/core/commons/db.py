"""
This module provides a simple dbmanager class that can be used for sqlite db interactions
"""
import sqlite3
from pathlib import Path
from typing import Dict, Tuple, List


class DbManager:
    """
    A class for managing the database operations

    """

    def __init__(self,logger):
        """
        Initializes the Database manager class object
        """
        self.database = Path('orders.db')


    def __repr__(self) -> str:
        """
        Returns a string representation of the DbManager object.

        Returns:
            str: A string representation of the DbManager object.
        """
        return "TODO : for later extensions"


    def __str__(self) -> str:
        """
        Returns a string representation of the DbManager object.

        Returns:
            str: A string representation of the DbManager object.
        """
        return "TODO : for later extensions"

    def _get_connection(self, database) -> sqlite3.Connection:
        """
        Returns a database connection.

        Returns:
            sqlite3.Connection : A database connection.
        """
        with sqlite3.connect(database) as conn:
            return conn

    def run_sql_with_values(self,sql: str,values: Dict) -> None:
        """
        TODO
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql,values)
            conn.commit()

    def run_sql(self,sql: str) -> None:
        """
        TODO
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

    def select (self,sql: str) -> [Tuple]:
        """
        TODO
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
        return cursor.fetchall()

    def select_one(self,sql: str) -> Tuple:
        """
        TODO
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
        return cursor.fetchone()
