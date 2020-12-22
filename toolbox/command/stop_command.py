import logging
import sys

from click import Argument, Context
from click import Option

from mutagen_helper.manager import Manager

from toolbox.command.abstract_command import AbstractCommand
from toolbox.command.abstract_virtual_machine_command import AbstractVirtualMachineCommand


class StopCommand(AbstractCommand, AbstractVirtualMachineCommand):
    """
    Stop command
    """

    def __init__(self):
        super().__init__('start')
        self.help = 'Stop a project'
        self.no_args_is_help = True
        self.params.append(Argument(['project'], required=True, default=None))
        self.params.append(Option(['--vm'], default=False, is_flag=True, help='Stop the vm too'))

    def invoke(self, ctx: Context):
        name: str = ctx.params.get('name')
        virtual_machine: bool = ctx.params.get('vm')
        if not self.exists(name):
            logging.error('Unable to find %s path', name)
            sys.exit(1)

        project_type = self.detect_project_type()
        if project_type is None:
            logging.error('Unable to determine %s project type', name)
            sys.exit(1)

        logging.info('Project type detected for %s is %s', name, project_type.name)
        if project_type.is_mutagened():
            logging.info("Mutagen configuration detected")
            mutagen_helper = Manager()
            mutagen_helper.down(path=project_type.get_folder(), project=name)

        logging.debug("Project virtual machine is %s", project_type.virtual_machine)
        if project_type.virtual_machine and virtual_machine:
            self.stop_virtual_machine(project_type.virtual_machine)

command = StopCommand()