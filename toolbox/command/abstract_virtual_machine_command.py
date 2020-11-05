import logging
import os
import sys
from abc import ABC

from toolbox.config import config
from toolbox.model.config.project_type import ProjectType
from toolbox.tool.ssh import try_ssh
from toolbox.tool.virtual_machine import get_virtual_machine_manager
from toolbox.model.config.virtual_machine import VirtualMachine


class AbstractVirtualMachineCommand(ABC):

    @staticmethod
    def get_virtual_machine(virtual_machine_name: str) -> VirtualMachine:
        """
        Get the selected virtual machine
        :param virtual_machine_name:
        :return: VirtualMachine
        """
        if virtual_machine_name not in config.get('virtual_machine').keys():
            logging.error('Unknown virtual_machine, valid ones are %s', ', '.join(config.get('virtual_machine').keys()))
            sys.exit(1)

        return config.get('virtual_machine').get(virtual_machine_name)

    @staticmethod
    def start_virtual_machine(virtual_machine_name: str):
        """
        Start the virtual machine
        :param virtual_machine_name: the name of the virtual machine
        """
        virtual_machine = AbstractVirtualMachineCommand.get_virtual_machine(virtual_machine_name)
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
        virtual_machine = AbstractVirtualMachineCommand.get_virtual_machine(virtual_machine_name)
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
        return os.path.isdir(AbstractVirtualMachineCommand.path(name))

    @staticmethod
    def detect_project_type():
        """
        Detect the type of the project
        :return:
        """
        cwd = os.getcwd()
        for type_name in config.get('project_type').keys():
            project_type: ProjectType = config.get('project_type').get(type_name)
            if project_type.get_folder() in cwd:
                return project_type
        return None
