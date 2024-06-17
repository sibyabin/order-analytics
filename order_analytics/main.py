"""
 TODO:
"""
#!/usr/bin/env python

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

from core.commons.logger import Logger
from core.commons.db import DbManager
from core.commons.utils import Utils
from core.commons.batch import Batch




class Loader:
    """
    A class for managing the Loader

    """

    def __init__(self):
        """
        Initializes the Loader class object
        """
        self.logger = Logger(__name__).get_logger()
        self.db = DbManager(self.logger)
        self.utils = Utils(self.logger,self.db)
        self.batch = Batch(self.logger,self.db)

    def __str__(self) -> str:
        """
        TODO : for any later implementations
        """
        pass



def main():
    """
    main function and entry point of the etl load process
    """
    loader = Loader()
    loader.logger.info("==================BATCH START =================")
    batch = loader.batch
    batch.create_batch()
    loader.logger.info(str(batch))
    loader.logger.info("==================BATCH END ===================")

if __name__ == "__main__":
    main()
