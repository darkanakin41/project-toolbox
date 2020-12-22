import os

import click

from toolbox.command.abstract.group_dynamic import GroupDynamic


class MainCommands(GroupDynamic):
    """
    List of main commands
    """

    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name=name, commands=commands, **attrs)
        self.params.append(click.Option(['--verbose', '-v'], default=False, is_flag=True, help='Add more details'))

    def get_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), 'command')


main = MainCommands()

if __name__ == '__main__':
    main()
