import logging
import os
import sys

from mutagen_helper.manager import Manager

from toolbox.command.abstract_command import AbstractCommand
from toolbox.config import config
from toolbox.model.config.project_type import ProjectType


class StartCommand(AbstractCommand):
    """
    Start command
    """

    def exec(self, **kwargs):
        name = kwargs.get('name')
        if not StartCommand.exists(name):
            logging.error("Unable to find %s path", name)
            sys.exit(1)

        project_type = StartCommand.detect_project_type()
        if project_type is None:
            logging.error("Unable to determine % project type", name)
            sys.exit(1)

        logging.info("Project type detected for %s is %s", name, project_type.name)
        if project_type.is_mutagened():
            logging.info("Mutagen configuration detected")
            mutagen_helper = Manager()
            mutagen_helper.up(path=project_type.get_folder(), project=name)

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
        return os.path.isdir(StartCommand.path(name))

    @staticmethod
    def detect_project_type():
        """
        Detect project type
        :return: The type of the project, or None if not found
        """
        cwd = os.getcwd()
        for type_name in config.get('project_type').keys():
            project_type: ProjectType = config.get('project_type').get(type_name)
            if project_type.get_folder() in cwd:
                return project_type
        return None
