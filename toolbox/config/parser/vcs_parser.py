from toolbox.config.parser.abstract_parser import AbstractParser
from toolbox.model.config.vcs import Vcs


class VcsParser(AbstractParser):
    """
    Parse vcs configuration
    """

    def __init__(self, config):
        super().__init__(config)

    def get_config_key(self) -> str:
        return 'vcs'

    def parse(self, config: dict):
        vcs_configs = config.get(self.get_config_key())

        vcss: dict = {}

        for vcs in vcs_configs.keys():
            vcs_config = vcs_configs[vcs]
            base_url = vcs_config.get('base_url')
            user = vcs_config.get('user')
            password = vcs_config.get('password')
            token = vcs_config.get('token')

            vcs = Vcs(vcs,
                      base_url,
                      user=user,
                      password=password,
                      token=token)

            vcss[vcs] = vcs

        self.parsed = vcss
