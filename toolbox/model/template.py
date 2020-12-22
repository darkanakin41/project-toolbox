from toolbox.tool.logger import logger
import os
import shutil
import stat
from distutils.dir_util import copy_tree

from git import Git, Repo

from toolbox.config import ConfigurationFile
from toolbox.model.config.project_type import ProjectType


class Template:
    """
    Template management tools
    """

    def __init__(self, name: str, path: str, project_type: ProjectType):
        self.name = name
        self.path = path
        self.project_type = project_type

    def is_git(self) -> bool:
        """
        Check if the template is a git repository or not
        :return: True if a git repo
        """
        return "git" in self.path or "https" in self.path

    def template_path(self):
        """
        Calculate the template directory
        :return: the template directory
        """
        if self.is_git():
            return os.path.join(ConfigurationFile.get_template_directory(),
                                self.project_type.name,
                                self.name)
        return os.path.join(ConfigurationFile.get_template_directory(),
                            self.path)

    def copy(self, target_folder: str):
        """
        Copy the template into the target folder
        :param target_folder: the target folder
        :return:
        """
        if self.is_git():
            self._copy_git(target_folder)
        else:
            self._copy_directory(target_folder)

    def _copy_directory(self, target_folder: str):
        """
        Copy the template folder into the target folder
        :param target_folder: the target folder
        :return:
        """
        template_directory = self.template_path()
        logger.debug("[Template.py] Copy files from %s to %s", template_directory, target_folder)
        copy_tree(template_directory, target_folder)

    def _copy_git(self, target_folder):
        """
        Copy the git template into the target folder
        :param target_folder: the target folder
        :return:
        """
        template_directory = self.template_path()

        if os.path.isdir(template_directory):
            logger.debug("[Template.py] Updating template from git")
            Git(template_directory).pull()
        else:
            logger.debug("[Template.py] Cloning template from git")
            Repo.clone_from(url=self.path, to_path=template_directory)

        self._copy_directory(target_folder)

        logger.debug("[Template.py] Removal of .git folder coming from template")
        shutil.rmtree(os.path.join(target_folder, '.git'),
                      onerror=lambda func, path, exc_info: (os.chmod(path, stat.S_IWRITE), os.unlink(path)))
