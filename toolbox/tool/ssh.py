from toolbox.tool.logger import logger
import socket
import time

from paramiko import BadHostKeyException, AuthenticationException, SSHException
from paramiko.client import SSHClient, AutoAddPolicy

from toolbox.model.config.virtual_machine import VirtualMachine


def try_ssh(virtual_machine: VirtualMachine, retries: int = 10):
    """
    Try to connect to a virtual machine using ssh
    :param virtual_machine: the virtual machine
    :param retries: the maximum of retries
    """
    retry = 0
    connected = False

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.load_system_host_keys()
    while retry < retries and not connected:
        try:
            logger.debug('Trying ssh connection to %s %s out of %s retries', virtual_machine.hostname, retry, retries)
            ssh.connect(virtual_machine.hostname,
                        port=virtual_machine.ssh_port,
                        username=virtual_machine.ssh_username,
                        password=virtual_machine.ssh_password)
            connected = True
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error):
            time.sleep(10)
        retry += 1

    if not connected:
        raise Exception('[{}] Unable to connect to the machine after {} tries'.format(virtual_machine.hostname, retry))
    logger.info('Connection established to %s after %d out of %d retries', virtual_machine.name, retry, retries)
