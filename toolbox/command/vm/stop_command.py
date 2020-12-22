import click

from toolbox.command.abstract.command import Command
from toolbox.command.abstract.command_virtual_machine import CommandVirtualMachine
from toolbox.config import config
from toolbox.tool.logger import logger


class StopCommand(Command, CommandVirtualMachine):
    """
    Stop command
    """

    def __init__(self):
        super().__init__('start')
        self.help = 'Stop the vm'
        self.add_project_type_argument()

    def invoke(self, ctx: click.Context):
        type_name: str = ctx.params.get('project_type')
        StopCommand.validate_project_type(type_name)

        project_type = config.get('project_type').get(type_name)

        logger.debug("Project Type virtual machine is %s", project_type.virtual_machine)
        if project_type.virtual_machine:
            self.stop_virtual_machine(project_type.virtual_machine)


command = StopCommand()
