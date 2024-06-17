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
        Returns a string representation of the Loader.

        Returns:
            str: A string representation of the Loader object.
        """
        return f"Custom Message from Loader"



def main():
    print("Hello from main() in main.py")
    loader = Loader()
    print(str(loader))
    batch = loader.batch
    batch.create_batch()
    # loader.logger.info(batch.batch_info)

if __name__ == "__main__":
    main()
