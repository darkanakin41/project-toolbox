from toolbox.model.config.vcs import Vcs
from toolbox.tool.vcs.abstract_vcs import AbstractVCS
from toolbox.tool.vcs.github_vcs import GithubVCS


def get_vcs(vcs_config: Vcs):
    """
    Get the right VCS for the given vcs_config
    :param vcs_config: the selected vcs_config
    :return: AbstractVcs or None if no match
    """
    if vcs_config.type == 'github':
        return GithubVCS(vcs_config)
    return None
