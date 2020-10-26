import logging
import sys
from abc import ABC, abstractmethod


class AbstractParser(ABC):
    """
    Abstract Parser
    """

    def __init__(self, config: dict):
        self.parsed = {}
        if config.get(self.get_config_key()) is None:
            logging.error("No project types configuration detected")
            sys.exit(1)
        else:
            self.parse(config)

    @abstractmethod
    def get_config_key(self) -> str:
        """
        Get the config key used
        :return: string
        """

    @abstractmethod
    def parse(self, config: dict):
        """
        Parse the content of the config and convert it into object
        :param config: the configuration to parse
        :return:
        """
