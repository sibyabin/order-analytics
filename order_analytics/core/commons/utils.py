"""
This module provides a simple utils class that can be used to define the common functions
"""

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List

import pandas as pd


class Utils:
    """
    A class for managing the utility functions

    """

    def __init__(self, logger, conf, db, batch):
        """
        Initializes the utils class object
        """
        self.logger = logger
        self.db = db
        self.config = conf
        self.configs = conf.configs
        self.batch = batch

    def __str__(self) -> str:
        """
        Returns a string representation of the Utils object.

        Returns:
            str: A string representation of the Utils object.
        """
        return "Custom message from Utils"

    def read_file(self, location, file_name) -> str:
        with open(f"{location}/{file_name}", "r") as f:
            return f.read()

    def create_all_tables(self, tables: [str]) -> None:
        """ """
        for table in tables:
            sql_ddls_path = self.config.sql_ddls_path
            file_name = f"{sql_ddls_path}/{table}.sql"
            sql = self.read_file(sql_ddls_path, f"{table}.sql")
            self.logger.info(f"Going to execute `{file_name}`")
            self.db.run_sql_file(sql)
            self.logger.info(f"{file_name} executed successfully")

    def load_mart_tables(self, tables: [str]) -> None:
        """
        function to load the mart tables which involves transformation logic
        """
        self.logger.info(f"Going to load Mart tables")
        for table in tables:
            sql_transformations_path = self.config.sql_transformations_path
            file_name = f"{sql_transformations_path}/{table}.sql"
            sql = self.read_file(sql_transformations_path, f"{table}.sql")
            for token, replacement_value in self.batch.batch_tokens.items():
                sql = sql.replace(token, replacement_value)

            self.logger.info(f"Going to execute `{file_name}`")
            self.logger.info(
                f""" SQL
                                {sql}
                              """
            )
            self.db.run_sql_file(sql)
            self.logger.info(f"{file_name} executed successfully")

    @staticmethod
    def get_quarter(month):
        quarter = (month - 1) // 3 + 1
        return f"Q{quarter}"

    def load_date_dim(self, start_date, end_date) -> None:
        """
        Function to load the date_dim table.
        date_dim dim will be truncated and loaded for the ranges mentioned in config.ini file
        the function will raise an error if the current date is not between start and end dates
        configured(missing date_dim entry)
        """

        self.logger.info(f"Going to load date_dim between {start_date} and {end_date}")
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        if not (start <= date.today() <= end):
            raise ValueError(f"Today's date is not between '{start}' and '{end}' ")
        self.logger.info("Today's date is within the specified range.")

        date_list = [
            (
                date,
                date.weekday(),
                date.strftime("%A"),
                date.day,
                date.month,
                self.get_quarter(date.month),
                date.year,
            )
            for date in (start + timedelta(days=x) for x in range((end - start).days + 1))
        ]

        # clean table
        self.db.run_sql("DELETE FROM date_dim WHERE 1=1;")

        with self.db._get_connection(self.db.database) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                """
                                INSERT INTO date_dim(full_date, week_day, weekday_name, day, month, quarter, year)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                               """,
                date_list,
            )
            conn.commit()

        self.logger.info(f"date_dim loaded between {start_date} and {end_date}")

    def read_csv(self, location, file_name, names) -> pd.DataFrame:
        df = pd.read_csv(f"{location}/{file_name}", dtype="str", names=names, skiprows=1)
        return df

    @staticmethod
    def replace_tokens_in_df(df, tokens: Dict) -> pd.DataFrame:
        """
        Replaces tokens in a DataFrame with corresponding values from a dictionary.

        This method iterates over the DataFrame and replaces occurrences of keys from the
        tokens dictionary with their corresponding values. The replacement is performed
        on all string columns in the DataFrame.

        Parameters:
        - df (pd.DataFrame): The DataFrame in which token replacement will be performed.
        - tokens (Dict): A dictionary where keys are tokens to be replaced and values are
          the replacement values.

        Returns:
        - pd.DataFrame: A new DataFrame with tokens replaced.
        """
        df.replace(tokens, regex=True)
        return df

    def load_stg_table(self, tables: str, file_columns: str, filename: str) -> None:
        """
        Loads data into a staging table from a file.

        This method reads data from the specified file and inserts it into the staging table
        corresponding to the provided table name. The file_columns parameter specifies the
        mapping of file columns to table columns.

        Parameters:
        - tables (str): The name of the staging table to which the data will be loaded.
        - file_columns (str): A string representing the column mapping from the file to the table.
        - filename (str): The path to the file containing the data to be loaded.

        Returns:
        - None
        """
        for table in tables:
            new_columns = [
                "order_number",
                "client_name",
                "product_name",
                "product_type",
                "unit_price",
                "product_quantity",
                "total_price",
                "currency",
                "delivery_address",
                "delivery_city",
                "delivery_postcode",
                "delivery_country",
                "delivery_contact_number",
                "payment_type",
                "payment_billing_code",
                "payment_date",
            ]
            df_src = self.read_csv(self.config.files_path, filename, new_columns)
            df_src["created_ts"] = datetime.today()
            df_src["created_id"] = self.batch.batch_id
            df = self.replace_tokens_in_df(df_src, self.batch.batch_tokens)
        with self.db._get_connection(self.db.database) as conn:
            df.to_sql(name=table, con=conn, if_exists="append", index=False)
