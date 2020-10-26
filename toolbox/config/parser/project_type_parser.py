from toolbox.config.parser.abstract_parser import AbstractParser
from toolbox.model.config.project_type import ProjectType
from toolbox.model.template import Template


class ProjectTypeParser(AbstractParser):
    """
    Parse project type configuration
    """

    def __init__(self, config):
        super().__init__(config)

    def get_config_key(self) -> str:
        return 'project_type'

    def parse(self, config: dict):
        project_types_config = config.get(self.get_config_key())

        project_types: dict = {}

        for type in project_types_config.keys():
            type_config = project_types_config[type]
            folder = type_config.get('folder')
            exec = type_config.get('exec')
            git = type_config.get('git')
            templates_config = type_config.get('templates')
            gitignore = type_config.get('gitignore')  # see https://github.com/github/gitignore

            project_type = ProjectType(type, folder, exec=exec, git=git, gitignore=gitignore)

            templates = {}
            if templates_config is not None:
                for template_name in templates_config.keys():
                    templates[template_name] = Template(template_name, templates_config[template_name], project_type)

            project_type.templates = templates

            project_types[type] = project_type

        self.parsed = project_types
