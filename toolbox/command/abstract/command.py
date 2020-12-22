import os
import sys
from abc import ABC

import click

from toolbox.model.config.project_type import ProjectType
from toolbox.config import config, project_type_names
from toolbox.tool.logger import logger


class Command(ABC, click.Command):
    """
    Abstract command
    """

    def invoke(self, ctx: click.Context):
        raise NotImplementedError()

    def add_project_type_argument(self):
        """
        Add project type to current arguments
        :return:
        """
        dpt = self.detect_project_type()
        if dpt is None:
            self.no_args_is_help = True
            self.params.append(click.Argument(['project_type'],
                                              required=True,
                                              type=click.Choice(project_type_names())))
        else:
            self.params.append(click.Argument(['project_type'],
                                              required=False,
                                              default=dpt.name,
                                              type=click.Choice(project_type_names())))

    @staticmethod
    def detect_project_type():
        """
        Detect the type of the project
        :return:
        """
        cwd = os.getcwd()
        for type_name in config.get('project_type').keys():
            project_type: ProjectType = config.get('project_type').get(type_name)
            if project_type.get_folder() in cwd:
                return project_type
        return None

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
            logger.error('Unknown project type, valid ones are %s', ', '.join(config.get('project_type').keys()))
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
            logger.error('Unknown vcs, valid ones are %s', ', '.join(config.get('vcs').keys()))
            if kill:
                sys.exit(1)
            return False
        return True
