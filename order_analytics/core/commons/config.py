"""
This module provides a simple config class that can be used to read the project configs
"""

import os
import sys
from configparser import ConfigParser
from typing import Dict


class Config:
    """
    A configuration class for the order analytics solution

    Attributes:
        config_file (str): The path to the INI configuration file.
        config (ConfigParser): The ConfigParser object.
    """

    def __init__(self, logger):
        """
        Initializes the Config object with the given configuration file path.

        """
        self.logger = logger
        self.config: ConfigParser = ConfigParser()
        self.project_home: str = self._get_project_home()
        self.config_path: str = f"{self.project_home}/config"
        self.db_path: str = f"{self.project_home}/database"
        self.sql_ddls_path: str = f"{self.project_home}/sqls/ddls"
        self.sql_transformations_path: str = f"{self.project_home}/sqls/transformations"
        self.files_path: str = f"{self.project_home}/files"
        self.config_filename: str = f"{self.project_home}/config/config.ini"
        self.configs: Dict = self.read_config()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Config object.

        Returns:
            str: A string representation of the Config object.
        """
        return f"""Config(config_file='{self.config_filename}',
                        project_home='{self.project_home}',
                        sql_ddls_path={self.sql_ddls_path},
                        files_path={self.files_path},
                        db_path={self.db_path}
                        )
                """

    def read_config(self) -> Dict[str, Dict[str, str]]:
        """
        Reads the project configuration file and returns the configuration as a dictionary.

        Returns:
            Dict[str, Dict[str, str]]: A dictionary with sections as keys and section configurations as values.
        Raises:
            FileNotFoundError: If the configuration file does not exist.
        """
        if not os.path.exists(self.config_filename):
            raise FileNotFoundError(f"The config file {self.config_filename} does not exist.")
        self.config.read(self.config_filename)
        return {section: dict(self.config.items(section)) for section in self.config.sections()}

    def _get_project_home(self) -> str:
        """
        Get the project_home

        Returns:
           str: project_home variable
        Raises:
            ValueError: If the PROJECT_HOME variable is not set.

        """
        project_home = os.getenv("PROJECT_HOME")
        if project_home is not None:
            self.logger.info(
                f"The value of the environment variable PROJECT_HOME is: {project_home}"
            )
        else:
            self.logger.info("The environment variable `PROJECT_HOME` is not set.")
            self.logger.info(
                "if you are not using make file, run export PROJECT_HOME=/path/to/order-analytics from terminal"
            )
            raise ValueError("Sorry, The environment variable `PROJECT_HOME` is not set.")
        return project_home


# # Usage
# config: Config = Config()
# print(config.configs)
