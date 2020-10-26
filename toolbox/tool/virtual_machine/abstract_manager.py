from abc import ABC, abstractmethod

from toolbox.model.config.virtual_machine import VirtualMachine


class AbstractManager(ABC):
    """
    Abstract Virtual Machine manager
    """

    def __init__(self, virtual_machine: VirtualMachine):
        self.virtual_machine = virtual_machine

    @abstractmethod
    def start(self):
        """
        Start the VM
        """

    @abstractmethod
    def stop(self):
        """
        Stop the VM
        """

    @abstractmethod
    def status(self):
        """
        Status of the VM
        """
