import logging
import os
import sys

import click
import click_log

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

plugin_folder = os.path.join(os.path.dirname(__file__), 'command')


class MainCommands(click.Group):
    """
    List of main commands
    """

    def list_commands(self, ctx):
        return ['create', 'start', 'stop', 'list']

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '_command.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['command']


main = MainCommands()

if __name__ == '__main__':
    main()
