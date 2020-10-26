from toolbox.config.parser.abstract_parser import AbstractParser
from toolbox.model.config.vcs import Vcs


class VcsParser(AbstractParser):
    """
    Parse vcs configuration
    """

    def get_config_key(self) -> str:
        return 'vcs'

    def parse(self, config: dict):
        vcs_configs = config.get(self.get_config_key())

        vcss: dict = {}

        for vcs_name in vcs_configs.keys():
            vcs_config = vcs_configs[vcs_name]
            base_url = vcs_config.get('base_url')
            vcs_type = vcs_config.get('type')
            user = vcs_config.get('user')
            password = vcs_config.get('password')
            token = vcs_config.get('token')

            vcs = Vcs(vcs_name,
                      vcs_type,
                      base_url,
                      user=user,
                      password=password,
                      token=token)

            vcss[vcs_name] = vcs

        self.parsed = vcss
