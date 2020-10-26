from toolbox.model.config.virtual_machine import VirtualMachine
from toolbox.tool.virtual_machine.vmware_manager import VmwareManager


def get_virtual_machine_manager(virtual_machine: VirtualMachine):
    """
    Get the right Manager for the given virtual_machine
    :param virtual_machine: the selected virtual_machine
    :return: AbstractManager or None if no match
    """
    if virtual_machine.type == 'vmware':
        return VmwareManager(virtual_machine)
    return None
