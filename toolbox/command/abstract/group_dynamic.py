import os
from abc import ABC, abstractmethod

import click


class GroupDynamic(ABC, click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name=name, commands=commands, **attrs)
        self.no_args_is_help = True

    @abstractmethod
    def get_path(self) -> str:
        """
        Get the path of the current command group
        :return:
        """
        pass

    def list_commands(self, ctx):
        commands = []
        for f in os.listdir(self.get_path()):
            if f.startswith('_') or f.startswith('abstract'):
                continue
            commands.append(f.replace('_command.py', ''))
        commands.sort()
        return commands

    def get_command(self, ctx, name):
        ns = {}
        if os.path.isdir(os.path.join(self.get_path(), name)):
            fn = os.path.join(self.get_path(), name, '__init__.py')
        else:
            fn = os.path.join(self.get_path(), name + '_command.py')

        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)

        try:
            return ns['command']
        except KeyError:
            return None
