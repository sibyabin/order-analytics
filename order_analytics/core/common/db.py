"""
This module provides a simple dbmanager class that can be used for sqlite db interactions
"""
import sqlite3
from pathlib import Path


class DbManager:
    """
    A class for managing the database operations

    """

    def __init__(self):
        """
        Initializes the Database manager class object
        """
        self.database = Path('./order_analytics/database/orders.db')
        self.conn, self.cursor = self._get_conn_cursor(self.database)



    def __repr__(self) -> str:
        """
        Returns a string representation of the DbManager object.

        Returns:
            str: A string representation of the DbManager object.
        """
        return "Custom messge"


    def _get_conn_cursor(self, database):
        """
        TODO

        """
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            return conn , cursor

    def _sample_table_test(self):
        """
        TODO

        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS movie(title, year, score)")
        self.cursor.execute("INSERT INTO movie VALUES ('ABC', 1975, 8.2),('XYZ', 1971, 7.5)")
        self.conn.commit()
        res = self.cursor.execute("SELECT * FROM movie")
        res.fetchall()

# Usage
db =  DbManager()
db._sample_table_test()
