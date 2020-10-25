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
