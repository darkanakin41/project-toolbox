from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    """
    Abstract command
    """

    @abstractmethod
    def exec(self, **kwargs):
        """
        Exec function
        :param kwargs: all needed arguments
        :return:
        """
