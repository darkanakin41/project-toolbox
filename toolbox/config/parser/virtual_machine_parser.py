from toolbox.config.parser.abstract_parser import AbstractParser
from toolbox.model.config.virtual_machine import VirtualMachine


class VirtualMachineParser(AbstractParser):
    """
    Parse vcs configuration
    """

    def get_config_key(self) -> str:
        return 'virtual_machine'

    def parse(self, config: dict):
        configs = config.get(self.get_config_key())

        parsed: dict = {}

        for config_name in configs.keys():
            conf = configs[config_name]
            path = conf.get('path')
            hostname = conf.get('hostname')
            ssh_username = conf.get('ssh_username')
            ssh_password = conf.get('ssh_password')
            ssh_port = conf.get('ssh_port')
            vm_type = conf.get('type')
            vm_exec = conf.get('exec')

            vcs = VirtualMachine(config_name,
                                 vm_type,
                                 vm_exec,
                                 path,
                                 hostname,
                                 ssh_username,
                                 ssh_password,
                                 ssh_port)

            parsed[config_name] = vcs

        self.parsed = parsed
