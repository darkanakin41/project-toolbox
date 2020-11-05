import logging
import sys

from mutagen_helper.manager import Manager

from toolbox.command.abstract_command import AbstractCommand
from toolbox.command.abstract_virtual_machine_command import AbstractVirtualMachineCommand


class StartCommand(AbstractCommand, AbstractVirtualMachineCommand):
    """
    Start command
    """

    def exec(self, **kwargs):
        name = kwargs.get('name')
        if not StartCommand.exists(name):
            logging.error("Unable to find %s path", name)
            sys.exit(1)

        project_type = self.detect_project_type()
        if project_type is None:
            logging.error("Unable to determine %s project type", name)
            sys.exit(1)

        logging.debug("Project virtual machine is %s", project_type.virtual_machine)
        if project_type.virtual_machine:
            self.start_virtual_machine(project_type.virtual_machine)

        logging.info("Project type detected for %s is %s", name, project_type.name)
        if project_type.is_mutagened():
            logging.info("Mutagen configuration detected")
            mutagen_helper = Manager()
            mutagen_helper.up(path=project_type.get_folder(), project=name)

        project_type.exec_commands(self.path(name))
