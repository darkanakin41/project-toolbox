from abc import ABC, abstractmethod


class AbstractCommand(ABC):

    @abstractmethod
    def exec(self, **kwargs):
        """
        Exec function
        :param kwargs: all needed arguments
        :return:
        """
        pass