"""
This module provides a simple dbmanager class that can be used for sqlite db interactions
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import os


class DbManager:
    """
    A class for managing the database operations
    """

    def __init__(self, logger,conf):
        """
        Initializes the Database manager class object
        """
        self.conf = conf
        self.database = Path(f"{self.conf.db_path}/orders.db")
        self.logger = logger


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

    def run_sql_with_values(self, sql: str, values: Dict) -> None:
        """
        Execute a SQL command with parameterized values in the database.

        This method is used to execute a SQL statement with placeholders, replacing them
        with values from the provided dictionary

        Parameters:
        sql (str): A SQL statement with placeholders for parameterized queries.
        values (Dict): A dictionary containing keys that match the placeholders in the SQL
                       statement and their corresponding values to be bound.

        Returns:
        None
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()

    def run_sql_file(self, sql_file: str) -> None:
        """
        Execute SQL commands from a file in the database.

        This method reads an SQL file and executes its contents against the database.
        It is typically used for running batch operations or schema migrations.

        Parameters:
        sql_file (str): The path to the SQL file containing SQL statements.

        Returns:
        None
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql_file)
            conn.commit()

    def run_sql(self, sql: str) -> None:
        """
        Execute a SQL command in the database.

        This method does not return anything. It is used to execute database operations
        that don't return data, such as INSERT, UPDATE, DELETE, etc.

        Parameters:
        sql (str): A SQL statement to be executed.

        Returns:
        None
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

    def select(self, sql: str) -> [Tuple]:
        """
        Execute a SQL query and return all the results.
        This method is used to execute a SELECT statement and return all rows of the result.

        Parameters:
        sql (str): A SQL query to retrieve data from the database.

        Returns:
        list of tuple: The rows returned by the query.
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
        return cursor.fetchall()

    def select_one(self, sql: str) -> Tuple:
        """
        Execute a SQL query and return a single result.

        This method is used to execute a SELECT statement and return only the first row of the result.
        If the query returns no results, it returns None.

        Parameters:
        sql (str): A SQL query to retrieve data from the database.

        Returns:
        tuple or None: The first row of the result or None if no results are found.
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
        return cursor.fetchone()
