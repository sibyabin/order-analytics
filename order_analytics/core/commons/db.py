"""
This module provides a simple dbmanager class that can be used for sqlite db interactions
"""
import sqlite3
from pathlib import Path
from typing import Dict


class DbManager:
    """
    A class for managing the database operations

    """

    def __init__(self,logger):
        """
        Initializes the Database manager class object
        """
        self.database = Path('orders.db')
        logger.info("Message from DbManager Init")
        logger.info(f"Database = {self.database}")


    def __repr__(self) -> str:
        """
        Returns a string representation of the DbManager object.

        Returns:
            str: A string representation of the DbManager object.
        """
        return "Custom message"


    def __str__(self) -> str:
        """
        Returns a string representation of the DbManager object.

        Returns:
            str: A string representation of the DbManager object.
        """
        return "Custom message STR"

    def _get_connection(self, database):
        """
        TODO
        """
        with sqlite3.connect(database) as conn:
            print(f"conn={conn}")
            return conn

    def run_sql_with_values(self,sql: str,values: Dict):
        """
        TODO
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql,values)
            conn.commit()

    def run_sql(self,sql: str):
        """
        TODO
        """
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

    def select (self,sql):
        """
        TODO
        """
        print("within select function")
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
        return cursor.fetchall()

    def select_one (self,sql):
        """
        TODO
        """
        print("within select_one function")
        with self._get_connection(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
        return cursor.fetchone()

    def _sample_insert(self):
        """
        TODO

        """
        conn = self._get_connection(self.database)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS movie(title, year, score)")
        cursor.execute("INSERT INTO movie VALUES ('ABC', 1975, 8.2),('XYZ', 1971, 7.5)")
        conn.commit()
        print(self.select("SELECT * FROM movie"))
