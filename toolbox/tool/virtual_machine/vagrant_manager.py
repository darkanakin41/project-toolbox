import logging
import os

from toolbox.tool.virtual_machine.abstract_manager import AbstractManager


class VagrantManager(AbstractManager):
    """
    Vmware Virtual Machine manager
    """
    def start(self):
        if self.status(output=False):
            logging.info('VM %s is up, nothing to do here', self.virtual_machine.name)
            return

        if not os.path.isfile(self.virtual_machine.path):
            logging.error('VM %s is not found on drive', self.virtual_machine.path)
            return

        os.popen('cd {} && "{}" up'.format(self.virtual_machine.exec, self.virtual_machine.path))
        logging.info('VM %s is now started', self.virtual_machine.name)

    def stop(self):
        if not self.status(output=False):
            logging.info('VM %s is down, nothing to do here', self.virtual_machine.name)
            return

        if not os.path.isfile(self.virtual_machine.path):
            logging.error('VM %s is not found on drive', self.virtual_machine.path)
            return

        os.popen('cd {} && "{}" halt'.format(self.virtual_machine.exec, self.virtual_machine.path))
        logging.info('VM %s is now stopped', self.virtual_machine.name)

    def status(self, output: bool = True):
        stream = os.popen('"{}" global-status nogui'.format(self.virtual_machine.exec))
        command_output = stream.read()
        rows = command_output.split('\n')

        status = filter(lambda row: self.virtual_machine.path.replace('\\', '/') in row and 'running' in row, rows)

        if output:
            if len(list(status)) == 1:
                logging.info('VM %s is up', self.virtual_machine.name)
            else:
                logging.info('VM %s is down', self.virtual_machine.name)

        return len(list(status)) == 1
