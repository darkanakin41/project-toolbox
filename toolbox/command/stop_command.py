import logging
import os
import sys

from mutagen_helper.manager import Manager

from toolbox.command.abstract_command import AbstractCommand
from toolbox.config import config
from toolbox.model.config.project_type import ProjectType
from toolbox.tool.virtual_machine import get_virtual_machine_manager


class StopCommand(AbstractCommand):
    """
    Stop command
    """

    def exec(self, **kwargs):
        name: str = kwargs.get('name')
        virtual_machine: bool = kwargs.get('vm')
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

        logging.debug("Project virtual machine is %s", project_type.virtual_machine)
        if project_type.virtual_machine and virtual_machine:
            self.stop_virtual_machine(project_type.virtual_machine)

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

    @staticmethod
    def stop_virtual_machine(virtual_machine_name: str):
        """
        Stop the virtual machine
        :param virtual_machine_name: the name of the virtual machine
        """
        if virtual_machine_name not in config.get('virtual_machine').keys():
            logging.error('Unknown virtual_machine, valid ones are %s', ', '.join(config.get('virtual_machine').keys()))
            sys.exit(1)

        virtual_machine = config.get('virtual_machine').get(virtual_machine_name)
        manager = get_virtual_machine_manager(virtual_machine)
        manager.stop()
