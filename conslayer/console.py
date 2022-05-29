# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Patrick Michl
# This file is part of Console Slayer, https://github.com/fishroot/conslayer
#
"""Console management."""

__copyright__ = '2022 Patrick Michl'
__license__ = 'MIT'
__docformat__ = 'google'
__author__ = 'Patrick Michl'
__email__ = 'patrick.michl@gmail.com'
__authors__ = ['Patrick Michl <patrick.michl@gmail.com>']

from typing import List, Optional

#
# MessageQueue
#

class MessageQueue(object):
    """MessageQueue class.
    
    Description:
        Stores messages for console output.

    Attributes:
        silent (readonly, bool): Flag to suppress console output

    Design Patterns:
        Behaviour Subject

    """

    __instance: Optional['MessageQueue'] = None
    __queue: List[str]
    __silent: bool = False

    @property
    def silent(self):
        return self.__silent
    
    @silent.setter
    def silent(self, silent: bool):
        self.__silent = silent

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
        """Queue a message.
        
        Args:
            message (str): Message to be queued
        
        """
        self.__queue.append(message)

    def flush(self):
        """Flush the message queue."""
        self.__queue = []

    def print(self):
        """Print the message queue."""
        if self.silent: return
        message = str(self)
        if message != "":
            print(message)
            self.flush()
