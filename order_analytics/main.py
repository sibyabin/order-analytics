#!/usr/bin/env python
"""
 TODO:
"""

import argparse
import logging
import os
import pprint
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

from order_analytics.core.commons.batch import Batch
from order_analytics.core.commons.config import Config
from order_analytics.core.commons.db import DbManager
from order_analytics.core.commons.logger import Logger
from order_analytics.core.commons.utils import Utils

# Define a logger object
logger = Logger(__name__).get_logger()


class Loader:
    """
    A class for managing the Loader

    """

    def __init__(self, conf, logger):
        """
        Initializes the Loader class object
        """
        self.logger = logger
        self.config = conf
        self.db = DbManager(self.logger)
        self.batch = Batch(self.logger, self.db)
        self.utils = Utils(self.logger, self.config, self.db, self.batch)

    def __str__(self) -> str:
        """
        TODO : for any later implementations
        """
        pass

    def _set_value(self, key, value):
        self.key = value


def main():
    """
    main function and entry point of the etl load process
    """
    environment = "dev"
    logger.info("==================BATCH START =================")

    # Define Config and Loggers
    conf = Config(logger)
    logger.info(str(conf))

    # Get tables from config
    table_list = conf.configs[environment]["tables"].split(",")
    logger.info(f"TABLES={table_list}")

    # Create the tables (if not exists) from .sql files
    loader = Loader(conf, logger)
    loader._set_value("environment", environment)
    loader.utils.create_all_tables(table_list)

    # Create the batch record
    batch = loader.batch
    batch.create_batch()
    loader.logger.info(str(batch))

    # Load the date_dimension table based on range stored in config
    start_date = conf.configs[environment]["date_dim_start"]
    end_date = conf.configs[environment]["date_dim_end"]
    loader.utils.load_date_dim(start_date, end_date)

    # Load the stage data
    stg_tables = conf.configs[environment]["stg_tables"].split(",")
    file_columns = conf.configs[environment]["file_columns"]
    loader.logger.info(f"STAGE TABLES TO LOAD = {stg_tables}")
    loader.utils.load_stg_table(stg_tables, file_columns, filename="orders.csv")

    # Load the Dimension tables
    dim_tables = conf.configs[environment]["dim_tables"].split(",")
    loader.logger.info(f"DIMENSION TABLES TO LOAD = {dim_tables}")
    loader.utils.load_mart_tables(dim_tables)

    # Load the fact tables
    fact_tables = conf.configs[environment]["fact_tables"].split(",")
    loader.logger.info(f"FACT TABLES TO LOAD = {fact_tables}")
    loader.utils.load_mart_tables(fact_tables)

    # update the batch_information table with status ='COMPLETED' and updated_ts , updated_batch_id
    batch.update_batch()
    logger.info("==================BATCH END ===================")


if __name__ == "__main__":
    main()
