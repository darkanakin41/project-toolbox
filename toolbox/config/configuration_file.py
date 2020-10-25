import os
import sys

import yaml


class ConfigurationFile:
    """
    Management of the configuration file
    """

    def __init__(self):
        self.config = None
        config_file = os.path.join(ConfigurationFile.base_folder(), "config.yaml")
        with open(config_file, "r") as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        if self.config is None:
            print("Please provide the right configuration")
            sys.exit()

    @staticmethod
    def base_folder():
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    @staticmethod
    def get_template_directory():
        """
        Retrieve the template directory
        :return:
        """
        return os.path.join(ConfigurationFile.base_folder(), "templates")
