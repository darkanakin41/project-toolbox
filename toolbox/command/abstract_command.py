import logging
import sys
from abc import ABC, abstractmethod

from toolbox.config import config


class AbstractCommand(ABC):
    """
    Abstract command
    """

    @abstractmethod
    def exec(self, **kwargs):
        """
        Exec function
        :param kwargs: all needed arguments
        :return:
        """

    @staticmethod
    def validate_project_type(type_name: str = None, kill: bool = True):
        """
        Validate that the given type is valid
        :param type_name: the type to check
        :param kill: wether it should kill the process or not
        :return: boolean
        """
        if type_name is None:
            return True

        if type_name not in config.get('project_type').keys():
            logging.error('Unknown project type, valid ones are %s', ', '.join(config.get('project_type').keys()))
            if kill:
                sys.exit(1)
            return False
        return True

    @staticmethod
    def validate_vcs_type(type_name: str = None, kill: bool = True):
        """
        Validate that the given type is valid
        :param type_name: the type to check
        :param kill: wether it should kill the process or not
        :return: boolean
        """
        if type is None:
            return True

        if type_name not in config.get('vcs').keys():
            logging.error('Unknown vcs, valid ones are %s', ', '.join(config.get('vcs').keys()))
            if kill:
                sys.exit(1)
            return False
        return True
