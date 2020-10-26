class VirtualMachine:
    """
    VmType configuration
    """

    def __init__(self,
                 name: str,
                 vm_type: str,
                 vm_exec: str,
                 vm_path: str,
                 hostname: str,
                 ssh_username: str,
                 ssh_password: str,
                 ssh_port: int):
        self.name = name
        self.type = vm_type
        self.exec = vm_exec
        self.path = vm_path
        self.hostname = hostname
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.ssh_port = ssh_port
