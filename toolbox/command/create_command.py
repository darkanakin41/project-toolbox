import logging
import os
import pathlib
import sys
import webbrowser
from configparser import NoSectionError

from git import Repo, InvalidGitRepositoryError
from toolbox.config import config
from toolbox.model.project import Project
from toolbox.model.template import Template
from toolbox.tool.vcs import get_vcs


class CreateCommand:
    def __init__(self):
        pass

    def exec(self, **kwargs):
        """
        Exec the command
        :param type: Project's type
        :param name: Project's name
        :param vcs: Project's vcs (default: none)
        :param template: Project's tempalte (default: none)
        :return:
        """
        type = kwargs.get('type')
        name = kwargs.get('name')
        vcs_type = kwargs.get('vcs')
        template = kwargs.get('template')

        if type not in config.get('project_type').keys():
            logging.error('Unknown type, valid ones are : {}'.format(', '.join(config.get('project_type').keys())))
            sys.exit(1)
        project_type = config.get('project_type').get(type)

        if vcs_type is None:
            vcs_config = None
        elif vcs_type not in config.get('vcs').keys():
            logging.error('Unknown vcs, valid ones are : {}'.format(', '.join(config.get('vcs').keys())))
            sys.exit(1)
        else:
            vcs_config = config.get('vcs').get(vcs_type)

        project = Project(name, project_type, vcs_config)

        self._create_folder(project=project)

        if template is not None:
            self._copy_template(project=project, template_name=template)

        repo_url = None
        repo_name = None
        vcs = None
        if vcs_config is not None:
            vcs = get_vcs(vcs_config=vcs_config)

        if vcs is not None:
            repo_url = vcs.create_project(project)
            repo_name = vcs.get_repository_name(project)
            gitignore_content = vcs.get_gitignore_template(project)

            if gitignore_content is not None:
                project.add_file('.gitignore', gitignore_content)

            project.add_file('README.md', '\n'.join([
                repo_name,
                '===',
                'This project have been generated with [darkanakin41/project-generator]'
                '(https://github.com/darkanakin41/project-generator)'
            ]))

        if repo_url is not None:
            CreateCommand._init_git(project, repo_url)

        if vcs is not None and repo_name is not None:
            webbrowser.open('/'.join([vcs.get_base_url(), repo_name]))

        project.exec_commands()

    @staticmethod
    def _create_folder(project: Project):
        """
        Create the folder for the given project
        :param project: the project
        """
        if project.exists():
            logging.info('Project already exist, no need to create the folder')
        else:
            pathlib.Path(project.get_path()).mkdir(parents=True, exist_ok=True)
            logging.info('Project folder created \'{}\''.format(project.get_path()))

    @staticmethod
    def _copy_template(project: Project, template_name: str):
        """
        Copy template files for the given project
        :param project: the project
        """
        if project.type.templates.get(template_name) is None:
            logging.error('Unknown template {}, valid ones are : {}'.format(template_name,
                                                                            ', '.join(project.type.templates.keys())))
            sys.exit(1)

        template: Template = project.type.templates.get(template_name)

        files = os.listdir(project.get_path())
        if len(files) > 0:
            logging.warning("Unable to copy template {} because project is already initialized".format(template.name))
            return

        template.copy(project.get_path())

    @staticmethod
    def _init_git(project: Project, repo_url: str = None):
        """
        Init the git repository in the folder
        :param repo_url: the url of the repository
        :return:
        """
        try:
            Repo(project.get_path())
            logging.info('This is already a git repository')
            return
        except InvalidGitRepositoryError:
            repo = Repo.init(project.get_path())
            logging.info('Initialization of git repository')

        CreateCommand._update_git_config(project, repo)

        origin = None
        if repo_url is not None:
            try:
                origin = repo.remote('origin')
                logging.info('Retrieving the origin remote')
            except NoSectionError:
                origin = repo.create_remote('origin', repo_url)
                logging.info('Adding the remote "origin" : {}'.format(repo_url))

        if len(repo.untracked_files) > 0:
            repo.git.add('.')
            logging.info('Staging new files')
        if repo.is_dirty():
            logging.info('Initial commit')
            repo.git.commit('-m "Initial commit"')
            if origin is not None:
                logging.info('Pushing files to remote')
                repo.git.push("--set-upstream", origin, repo.head.ref)

    @staticmethod
    def _update_git_config(project: Project, repo: Repo):
        if project.type.git is None:
            return

        configuration = project.type.git
        for section_key in configuration.keys():
            section = configuration[section_key]
            for option_key in section.keys():
                repo.config_writer().set_value(section_key, option_key, section[option_key])
