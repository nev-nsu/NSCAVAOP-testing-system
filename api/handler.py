from abc import ABCMeta, abstractmethod


class IHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, TRequestHandler):
        """Handle request"""
