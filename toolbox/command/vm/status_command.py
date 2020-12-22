import click

from toolbox.command.abstract.command import Command
from toolbox.command.abstract.command_virtual_machine import CommandVirtualMachine
from toolbox.config import config
from toolbox.tool.virtual_machine import get_virtual_machine_manager


class StatusCommand(Command, CommandVirtualMachine):
    """
    Start command
    """

    def __init__(self):
        super().__init__('start')
        self.help = 'Status of the vm'
        self.add_project_type_argument()

    def invoke(self, ctx: click.Context):
        type_name: str = ctx.params.get('project_type')
        StatusCommand.validate_project_type(type_name)

        project_type = config.get('project_type').get(type_name)
        if project_type.virtual_machine is None:
            print('No virtual machine for given project type')
            return

        virtual_machine = self.get_virtual_machine(project_type.virtual_machine)
        manager = get_virtual_machine_manager(virtual_machine)
        if manager.status(False):
            print("VM " + virtual_machine.name + " is on")
        else:
            print("VM " + virtual_machine.name + " is off")


command = StatusCommand()
