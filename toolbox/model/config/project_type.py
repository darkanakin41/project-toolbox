import os


class ProjectType:
    """
    Project Type Configuration
    """

    def __init__(self,
                 name: str,
                 folder: str,
                 exec: str = None,
                 templates: dict = dict({}),
                 git: dict = dict({}),
                 gitignore: str = None):
        self.name = name
        self.folder = folder
        self.exec = exec
        self.templates = templates
        self.git = git
        self.gitignore = gitignore

    def get_folder(self) -> str:
        """
        Get the absolute folder of the project type
        :return:
        """
        from toolbox.config import config
        return os.path.join(config.get('base_folder'), self.folder)
