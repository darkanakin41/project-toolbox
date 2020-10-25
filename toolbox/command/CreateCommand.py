import logging
import pathlib
import sys

from toolbox.config import config
from toolbox.model.project import Project


class CreateCommand:
    def __init__(self):
        pass

    def exec(self, **kwargs):
        type = kwargs.get('type')
        name = kwargs.get('name')
        vcs = kwargs.get('vcs')
        template = kwargs.get('template')

        if type not in config.get('project_type').keys():
            logging.error('Unknown type, valid ones are : {}'.format(', '.join(config.get('project_type').keys())))
            sys.exit(1)
        project_type = config.get('project_type').get(type)

        if vcs is None:
            vcs_config = None
        elif vcs not in config.get('vcs').keys():
            logging.error('Unknown vcs, valid ones are : {}'.format(', '.join(config.get('vcs').keys())))
            sys.exit(1)
        else:
            vcs_config = config.get('vcs').get(vcs)

        project = Project(name, project_type, vcs_config)

        self._create_folder(project=project)

        if template is not None:
            self._copy_template(project=project, template=template)

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
    def _copy_template(project: Project, template: str):
        """
        Copy template files for the given project
        :param project: the project
        """
        # TODO Template Management

        if template not in project.type.templates.keys():
            logging.error('Unknown template {}, valid ones are : {}'.format(template,
                                                                            ', '.join(project.type.templates.keys())))
            sys.exit(1)
