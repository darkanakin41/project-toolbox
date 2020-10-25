import logging
import sys

import click

from toolbox.__version__ import __version__
from toolbox.command.CreateCommand import CreateCommand


class SpecialHelpOrder(click.Group):
    def __init__(self, *args, **kwargs):
        self.help_priorities = {}
        super(SpecialHelpOrder, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        self.list_commands = self.list_commands_for_help
        return super(SpecialHelpOrder, self).get_help(ctx)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = super(SpecialHelpOrder, self).list_commands(ctx)
        return (c[1] for c in sorted(
            (self.help_priorities.get(command, 1), command)
            for command in commands))

    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` except capture
        a priority for listing command names in help.
        """
        help_priority = kwargs.pop('help_priority', 1)
        help_priorities = self.help_priorities

        def decorator(f):
            cmd = super(SpecialHelpOrder, self).command(*args, **kwargs)(f)
            help_priorities[cmd.name] = help_priority
            return cmd

        return decorator


@click.group(context_settings=dict(help_option_names=['-h', '--help']), cls=SpecialHelpOrder)
@click.version_option(prog_name='project-toolbox', version=__version__)
@click.option('-v', '--verbose', default=False, is_flag=True, help="Add more output")
@click.option('-s', '--silent', default=False, is_flag=True, help="No output at all")
def main(verbose, silent):
    """
    Main command group
    :return:
    """
    if not silent:
        root = logging.getLogger()
        if verbose:
            root.setLevel(logging.DEBUG)
        else:
            root.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)


@main.command(help='Create a new project', help_priority=1)
@click.argument('name', required=True)
@click.argument('type', required=True)
@click.option('--vcs', required=False)
@click.option('--template', required=False)
def create(name: str, type: str, vcs: str = None, template: str = None):
    command = CreateCommand()
    command.exec(name=name, type=type, vcs=vcs, template=template)


if __name__ == '__main__':
    main()
