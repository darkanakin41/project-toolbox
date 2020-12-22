import logging
import os

from mutagen_helper.manager import Manager


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
        self.mutagen_entries = None

    def get_folder(self) -> str:
        """
        Get the absolute folder of the project type
        :return:
        """
        from toolbox.config import config
        return os.path.join(config.get('base_folder'), self.folder)

    def get_projects(self) -> list:
        """
        Get all projects for the given type
        :return:
        """
        from toolbox.model.project import Project
        return [Project(f, self) for f in os.listdir(self.get_folder()) if
                not f.startswith(tuple(['.', '$'])) and os.path.isdir(os.path.join(self.get_folder(), f))]

    def is_mutagened(self) -> bool:
        """
        Check if the current type of project have mutagen configuratio
        :return:
        """
        return os.path.isfile(os.path.join(self.get_folder(), '.mutagen-helper.yml'))

    def get_mutagen_entries(self) -> []:
        """
        Get the current project_type mutagen entries
        :return:
        """
        if self.mutagen_entries is None:
            self.refresh_mutagen_entries()

        return self.mutagen_entries

    def get_mutagen_entry(self, project_name: str):
        """
        Get the project_name data
        :return: None or Mutagen Helper entry
        """
        entries = self.get_mutagen_entries()

        entry = list(filter(lambda x: x['Mutagen Helper']['Project name'] == project_name, entries))

        if len(entry) != 1:
            return None
        return entry[0]

    def refresh_mutagen_entries(self):
        """
        Refresh current mutagen data
        :return:
        """
        if not self.is_mutagened():
            self.mutagen_entries = []
            return

        mutagen_helper = Manager()
        self.mutagen_entries = mutagen_helper.list(path=self.get_folder())

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
