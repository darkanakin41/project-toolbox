from toolbox.config.configuration_file import ConfigurationFile
from toolbox.config.parser.project_type_parser import ProjectTypeParser
from toolbox.config.parser.vcs_parser import VcsParser
from toolbox.config.parser.virtual_machine_parser import VirtualMachineParser

file_config = ConfigurationFile().config

parsers = {
    'project_type': ProjectTypeParser(config=file_config),
    'vcs': VcsParser(config=file_config),
    'virtual_machine': VirtualMachineParser(config=file_config)
}
