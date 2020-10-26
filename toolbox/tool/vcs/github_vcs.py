from github import Github, GithubException
from toolbox.model.config.vcs import Vcs
from toolbox.model.project import Project
from toolbox.tool.vcs.abstract_vcs import AbstractVCS


class GithubVCS(AbstractVCS):
    """
    Github management functions
    """

    def __init__(self, vcs: Vcs):
        super().__init__()
        self.vcs = vcs
        if vcs.token:
            self.connector = Github(login_or_token=self.vcs.token)
        else:
            self.connector = Github(login_or_token=self.vcs.user, password=self.vcs.password)

    @staticmethod
    def get_base_url():
        return 'https://www.github.com'

    def get_repository_name(self, project: Project) -> str:
        return "{}/{}".format(self.vcs.user, project.name)

    def get_gitignore_template_from_connector(self, template: str) -> str:
        return self.connector.get_gitignore_template(template).source

    def create_project(self, project: Project) -> str:
        repository_name = self.get_repository_name(project)
        repo = None
        try:
            repo = self.connector.get_repo(repository_name)
        except GithubException:
            pass

        user = self.connector.get_user()
        if repo is None:
            repo = user.create_repo(project.name)
        repo.edit(description="This is a project generated using darkanakin41/project-generator",
                  private=True)

        return repo.ssh_url
