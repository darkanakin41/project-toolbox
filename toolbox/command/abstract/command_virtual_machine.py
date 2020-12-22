import os
import sys
from abc import ABC

from toolbox.config import config
from toolbox.model.config.project_type import ProjectType
from toolbox.model.config.virtual_machine import VirtualMachine
from toolbox.tool.logger import logger
from toolbox.tool.ssh import try_ssh
from toolbox.tool.virtual_machine import get_virtual_machine_manager


class CommandVirtualMachine(ABC):

    @staticmethod
    def get_virtual_machine(virtual_machine_name: str) -> VirtualMachine:
        """
        Get the selected virtual machine
        :param virtual_machine_name:
        :return: VirtualMachine
        """
        if virtual_machine_name not in config.get('virtual_machine').keys():
            logger.error('Unknown virtual_machine, valid ones are %s', ', '.join(config.get('virtual_machine').keys()))
            sys.exit(1)

        return config.get('virtual_machine').get(virtual_machine_name)

    @staticmethod
    def start_virtual_machine(virtual_machine_name: str):
        """
        Start the virtual machine
        :param virtual_machine_name: the name of the virtual machine
        """
        virtual_machine = CommandVirtualMachine.get_virtual_machine(virtual_machine_name)
        manager = get_virtual_machine_manager(virtual_machine)
        manager.start()

        if virtual_machine.hostname:
            try_ssh(virtual_machine)

    @staticmethod
    def stop_virtual_machine(virtual_machine_name: str):
        """
        Stop the virtual machine
        :param virtual_machine_name: the name of the virtual machine
        """
        virtual_machine = CommandVirtualMachine.get_virtual_machine(virtual_machine_name)
        manager = get_virtual_machine_manager(virtual_machine)
        manager.stop()

    @staticmethod
    def path(name: str) -> str:
        """
        Generate the path
        :param name: the name of the project
        :return: the full path of the project
        """
        return os.path.join(os.getcwd(), name)

    @staticmethod
    def exists(name: str) -> bool:
        """
        Check if the project exists
        :param name: the name of the project
        :return: True if exists, False if not
        """
        return os.path.isdir(CommandVirtualMachine.path(name))
