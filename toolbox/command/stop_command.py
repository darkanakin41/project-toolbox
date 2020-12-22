import sys

import click
from mutagen_helper.manager import Manager

from toolbox.command.abstract.command import Command
from toolbox.command.abstract.command_virtual_machine import CommandVirtualMachine
from toolbox.tool.logger import logger


class StopCommand(Command, CommandVirtualMachine):
    """
    Stop command
    """

    def __init__(self):
        super().__init__('start')
        self.help = 'Stop a project'
        self.no_args_is_help = True
        self.params.append(click.Argument(['project'], required=True, default=None))
        self.params.append(click.Option(['--vm'], default=False, is_flag=True, help='Stop the vm too'))

    def invoke(self, ctx: click.Context):
        name: str = ctx.params.get('project')
        virtual_machine: bool = ctx.params.get('vm')
        if not self.exists(name):
            logger.error('Unable to find %s path', name)
            sys.exit(1)

        project_type = self.detect_project_type()
        if project_type is None:
            logger.error('Unable to determine %s project type', name)
            sys.exit(1)

        logger.info('Project type detected for %s is %s', name, project_type.name)
        if project_type.is_mutagened():
            logger.info("Mutagen configuration detected")
            mutagen_helper = Manager()
            mutagen_helper.down(path=project_type.get_folder(), project=name)

        logger.debug("Project virtual machine is %s", project_type.virtual_machine)
        if project_type.virtual_machine and virtual_machine:
            self.stop_virtual_machine(project_type.virtual_machine)


command = StopCommand()
