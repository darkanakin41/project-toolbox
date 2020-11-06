import logging
import sys

import click

from toolbox.__version__ import __version__
from toolbox.command.create_command import CreateCommand
from toolbox.command.start_command import StartCommand
from toolbox.command.stop_command import StopCommand


class SpecialHelpOrder(click.Group):
    """
    The special help order
    """

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
@click.argument('project_type', required=True)
@click.option('--vcs', required=False)
@click.option('--template', required=False)
def create(name: str, project_type: str, vcs: str = None, template: str = None):
    """
    Create command
    :param name: The name of the project
    :param type: The type of the project
    :param vcs: The VCS to use
    :param template: The template to clone
    :return:
    """
    command = CreateCommand()
    command.exec(name=name, type=project_type, vcs=vcs, template=template)


@main.command(help='Start a project', help_priority=1)
@click.argument('name', required=True)
@click.option('--noexec', required=False, default=False, is_flag=True)
def start(name: str, noexec: bool):
    """
    Start command
    :param name: the name of the project
    :return:
    """
    command = StartCommand()
    command.exec(name=name, noexec=noexec)


@main.command(help='Stop a project', help_priority=1)
@click.argument('name', required=True)
@click.option('--vm', required=False, default=False, is_flag=True)
def stop(name: str, vm: bool):
    """
    Stop command
    :param name: the name of the project
    :param vm: if the vm is stopped as well
    :return:
    """
    command = StopCommand()
    command.exec(name=name, vm=vm)


if __name__ == '__main__':
    main(False, False)
