from abc import ABC, abstractmethod

from toolbox.config import config
from toolbox.model.project import Project


class AbstractVCS(ABC):
    """
    VCS Management Class
    """

    def __init__(self):
        self.connector = None

    def get_gitignore_template(self, project: Project) -> str:
        """
        Retrieve the gitignore template for the given project
        :param project: The project
        :return: the content of the gitignore
        """
        gitignore_content = []
        if project.type.gitignore is not None:
            gitignore_content.append(self.get_gitignore_template_from_connector(project.type.gitignore))
        if config.get('gitignore') is not None:
            gitignore_content.extend(config.get('gitignore'))
        return '\n'.join(gitignore_content)

    @staticmethod
    @abstractmethod
    def get_base_url() -> str:
        """
        Retrieve the base url
        :return:
        """

    @abstractmethod
    def get_gitignore_template_from_connector(self, template: str) -> str:
        """
        Retrieve the gitignore template from the connector
        :return:
        """

    @abstractmethod
    def get_repository_name(self, project: Project) -> str:
        """
        Retrieve the full repository name
        :param project: The project
        :return: the full repository name
        """

    @abstractmethod
    def create_project(self, project: Project) -> str:
        """
        Create the right repository for the given project
        :param project: The project
        :return: the url
        """
