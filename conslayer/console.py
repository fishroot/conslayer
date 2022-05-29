import reactivex as rx
from typing import Any, Iterator, List, Optional, OrderedDict

class MessageQueue(object):
    """
    MessageQueue class.
    
    Description:
        Stores messages for console output.

    Design Patterns:
        Behaviour Subject

    """

    __instance: Optional['MessageQueue'] = None
    __queue: List[str]

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.__queue = []
        return cls.__instance

    def __str__(self):
        if len(self.__queue) == 0:
            return ""
        return "\n".join(self.__queue)

    def queue(self, message: str):
        self.__queue.append(message)

    def flush(self):
        self.__queue = []

    def print(self):
        message = str(self)
        if message != "":
            print(message)
            self.flush()