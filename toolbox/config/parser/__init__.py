from toolbox.config.configuration_file import ConfigurationFile
from toolbox.config.parser.project_type_parser import ProjectTypeParser
from toolbox.config.parser.vcs_parser import VcsParser

file_config = ConfigurationFile().config

parsers = {
    'project_type': ProjectTypeParser(config=file_config),
    'vcs': VcsParser(config=file_config)
}
