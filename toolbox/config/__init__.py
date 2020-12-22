from toolbox.config.configuration_file import ConfigurationFile
from toolbox.config.parser import parsers
from toolbox.config.parser.abstract_parser import AbstractParser

config = {
    'base_folder': ConfigurationFile().config.get('base_folder'),
    'gitignore': ConfigurationFile().config.get('gitignore')
}

for parser_name in parsers.keys():
    parser: AbstractParser = parsers[parser_name]
    config[parser_name] = parser.parsed


def project_type_names():
    return [t[1].name for t in config.get('project_type').items()]


def vcs_names():
    return [v[1].name for v in config.get('vcs').items()]

