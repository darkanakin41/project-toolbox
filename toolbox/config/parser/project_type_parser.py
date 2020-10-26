from toolbox.config.parser.abstract_parser import AbstractParser
from toolbox.model.config.project_type import ProjectType
from toolbox.model.template import Template


class ProjectTypeParser(AbstractParser):
    """
    Parse project type configuration
    """

    def get_config_key(self) -> str:
        return 'project_type'

    def parse(self, config: dict):
        project_types_config = config.get(self.get_config_key())

        project_types: dict = {}

        for project_type_name in project_types_config.keys():
            type_config = project_types_config[project_type_name]
            folder = type_config.get('folder')
            exec_command = type_config.get('exec')
            git = type_config.get('git')
            virtual_machine = type_config.get('virtual_machine')
            templates_config = type_config.get('templates')
            gitignore = type_config.get('gitignore')  # see https://github.com/github/gitignore

            project_type = ProjectType(project_type_name,
                                       folder,
                                       exec_command=exec_command,
                                       git=git,
                                       gitignore=gitignore,
                                       virtual_machine=virtual_machine)

            templates = {}
            if templates_config is not None:
                for template_name in templates_config.keys():
                    templates[template_name] = Template(template_name, templates_config[template_name], project_type)

            project_type.templates = templates

            project_types[project_type_name] = project_type

        self.parsed = project_types
