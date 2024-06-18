"""
This module provides a simple Batch class that can be used to deal batch creation and updation
"""

import sqlite3
from datetime import date, datetime
from pathlib import Path


class Batch:
    """
    A class for managing the database operations
    """

    def __init__(self, logger, db):
        """
        Initializes the Database manager class object
        """
        self.logger = logger
        self.db = db
        self.batch_starttime = datetime.now()
        self.batch_date = date.today()
        self.batch_number = self._get_batch_number()
        self.batch_id = (
            f"{self.batch_date.strftime('%Y%m%d')}_{str(self.batch_number).zfill(4)}_ETL"
        )
        self.batch_status = "STARTED"
        self.batch_created_ts = self.batch_starttime
        self.batch_created_id = self.batch_id
        self.batch_tokens = {
            "{CREATED_BATCH_ID}": self.batch_created_id,
            "{UPDATED_BATCH_ID}": self.batch_created_id,
        }

    def __repr__(self) -> str:
        """
        TODO : for any later implementations
        """
        pass

    def __str__(self) -> str:
        """
        Returns a string representation of the Batch object.

        Returns:
            str: A string representation of the Batch object.
        """
        return f"(batch_id={self.batch_id}, batch_date={self.batch_date} batch_status={self.batch_status}, batch_starttime={self.batch_starttime})"

    def create_batch(self):
        """
        Initialize a new batch operation.

        This method sets up the necessary seed entries in batch_information table.

        Returns:
        None
        """
        try:
            self.logger.info("Going to create batch")
            self.db.run_sql_with_values(
                """ INSERT INTO batch_information VALUES
                                        (
                                            :id,
                                            :batch_id,
                                            :batch_date,
                                            :batch_number,
                                            :batch_status,
                                            :batch_starttime,
                                            :batch_endtime,
                                            :batch_created_ts,
                                            :batch_updated_ts,
                                            :batch_created_id,
                                            :batch_updated_id


                                        )""",
                {
                    "batch_id": self.batch_id,
                    "batch_date": self.batch_date,
                    "batch_number": self.batch_number,
                    "batch_status": self.batch_status,
                    "batch_starttime": self.batch_starttime,
                    "batch_created_ts": self.batch_created_ts,
                    "batch_created_id": self.batch_created_id,
                    "id": None,
                    "batch_updated_ts": None,
                    "batch_endtime": None,
                    "batch_updated_id": None,
                },
            )
            self.logger.info(f"Batch created with batch_id = {self.batch_created_id}")
        except sqlite3.OperationalError as e:
            self.logger.info("An operational error occurred:", str(e))

    def _get_batch_number(self) -> int:
        """
        Retrieve the current batch number.

        This private method is used to get the number associated with the current batch operation.

        Returns:
        int: The current batch number.
        """
        batch_num = 1
        try:
            batch_num = self.db.select_one(
                f""" SELECT COALESCE(max(batch_number),0)+1 AS batch_number
                                                   FROM batch_information
                                                WHERE batch_date = '{self.batch_date}'
                                        """
            )[0]
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                self.logger.info("The table batch_information does not exist.")
                self.logger.info("Going to create the table `batch_information`")
                self.db.run_sql(
                    """
                                    CREATE TABLE IF NOT EXISTS batch_information
                                    (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        batch_id varchar(20) NOT NULL,
                                        batch_date date NOT NULL,
                                        batch_number integer NOT NULL,
                                        batch_status varchar(20) NOT NULL,
                                        batch_starttime timestamp NOT NULL,
                                        batch_endtime timestamp DEFAULT NULL,
                                        batch_created_ts timestamp NOT NULL,
                                        batch_updated_ts timestamp  DEFAULT NULL,
                                        batch_created_id varchar(15) NOT NULL,
                                        batch_updated_id varchar(15) DEFAULT NULL
                                    )
                                """
                )
            else:
                self.logger.info("A SQLite operational error occurred:", str(e))
        return batch_num

    def update_batch(self) -> None:
        """
        Update the batch_information table.

        Returns:
        None
        """
        self.logger.info("Going to update the batch_information table")
        sql = f""" UPDATE batch_information
                        SET batch_status='COMPLETED', batch_endtime=CURRENT_TIMESTAMP, batch_updated_ts=CURRENT_TIMESTAMP, batch_updated_id ='{self.batch_id}'
                   WHERE batch_created_id = '{self.batch_id}'
            """
        self.logger.info(sql)
        self.db.run_sql(sql)
