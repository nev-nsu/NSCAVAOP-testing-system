from abc import ABCMeta, abstractmethod


class IHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, handler):
        """Handle request"""
