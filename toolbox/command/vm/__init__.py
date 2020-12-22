import os
import sys
import traceback

from toolbox.command.abstract.group_dynamic import GroupDynamic


class VmCommands(GroupDynamic):
    """
    List of main commands
    """

    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.help = "Virtual Machine related action"

    def get_path(self) -> str:
        try:
            raise NotImplementedError("No error")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            filename = traceback.extract_tb(exc_traceback)[-1].filename
        return os.path.dirname(filename)


command = VmCommands()
