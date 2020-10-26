import logging
import os


class ProjectType:
    """
    Project Type Configuration
    """

    def __init__(self,
                 name: str,
                 folder: str,
                 exec_command: str = None,
                 templates: dict = dict(),
                 git: dict = dict(),
                 gitignore: str = None,
                 virtual_machine: str = None):
        self.name = name
        self.folder = folder
        self.exec = exec_command
        self.templates = templates
        self.git = git
        self.gitignore = gitignore
        self.virtual_machine = virtual_machine

    def get_folder(self) -> str:
        """
        Get the absolute folder of the project type
        :return:
        """
        from toolbox.config import config
        return os.path.join(config.get('base_folder'), self.folder)

    def is_mutagened(self) -> bool:
        """
        Check if the current type of project have mutagen configuratio
        :return:
        """
        return os.path.isfile(os.path.join(self.get_folder(), '.mutagen-helper.yml'))

    def exec_commands(self, path: str = '.'):
        """
        Execute the commands
        :param path: the path to execute the command into
        :return: void
        """
        commands = self.exec
        if commands is not None and isinstance(commands, str):
            self._exec_command(commands, path)
        elif commands is not None and isinstance(commands, list):
            for command in commands:
                self._exec_command(command, path)

    @staticmethod
    def _exec_command(command: str, path: str = '.'):
        """
        Execute the command
        :param command: execute the given command in the project folder
        :return:
        """
        logging.info("Execution of %s command", command)
        os.system("{} {}".format(command, path))
