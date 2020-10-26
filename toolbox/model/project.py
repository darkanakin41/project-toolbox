import logging
import os

from toolbox.model.config.project_type import ProjectType
from toolbox.model.config.vcs import Vcs


class Project:
    """
    Class to describe and manage a project
    """

    def __init__(self, name, project_type: ProjectType, vcs: Vcs = None):
        self.name = name
        self.type = project_type
        self.vcs = vcs

    def get_path(self) -> str:
        """
        Get the project path
        :return: the absolute project path
        """
        return os.path.join(self.type.get_folder(), self.name)

    def exists(self) -> bool:
        """
        Check if the project already exists
        :return: True if exist, and False if not
        """
        return os.path.exists(self.get_path())

    def is_git_initialized(self):
        """
        Check if the .git repository exist
        :return:
        """
        return os.path.isdir(os.path.join(self.get_path(), '.git'))

    def add_file(self, filename, content):
        """
        Create the given filename in the folder with given content
        :param filename: the name of the file to create
        :param content: the content of the file
        :return:
        """
        with open(os.path.join(self.get_path(), filename), "w") as stream:
            stream.write(content)

    def exec_commands(self):
        """
        Execute the commands
        :return: void
        """
        commands = self.type.exec
        if commands is not None and isinstance(commands, str):
            self._exec_command(commands)
        elif commands is not None and isinstance(commands, list):
            for command in commands:
                self._exec_command(command)

    def _exec_command(self, command: str):
        """
        Execute the command
        :param command: execute the given command in the project folder
        :return:
        """
        project_dir = self.get_path()
        logging.info("Execution of {}".format(command))
        os.system("{} {}".format(command, project_dir))
