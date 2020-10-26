import logging
import os
import sys

from mutagen_helper.manager import Manager

from toolbox.command.abstract_command import AbstractCommand
from toolbox.config import config
from toolbox.model.config.project_type import ProjectType


class StopCommand(AbstractCommand):
    """
    Stop command
    """

    def exec(self, **kwargs):
        name = kwargs.get('name')
        if not StopCommand.exists(name):
            logging.error('Unable to find %s path', name)
            sys.exit(1)

        project_type = StopCommand.detect_project_type()
        if project_type is None:
            logging.error('Unable to determine %s project type', name)
            sys.exit(1)

        logging.info('Project type detected for %s is %s', name, project_type.name)
        if project_type.is_mutagened():
            logging.info("Mutagen configuration detected")
            mutagen_helper = Manager()
            mutagen_helper.down(path=project_type.get_folder(), project=name)

        project_type.exec_commands(self.path(name))

    @staticmethod
    def path(name: str) -> str:
        """
        Generate the path
        :param name: the name of the project
        :return: the full path of the project
        """
        return os.path.join(os.getcwd(), name)

    @staticmethod
    def exists(name: str) -> bool:
        """
        Check if the project exists
        :param name: the name of the project
        :return: True if exists, False if not
        """
        return os.path.isdir(StopCommand.path(name))

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
