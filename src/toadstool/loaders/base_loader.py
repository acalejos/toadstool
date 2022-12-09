from abc import ABC, abstractmethod, abstractclassmethod

class Loader(ABC):
    """
    Used to import files into a Python dict
    """
    def __init__(self, path):
        """Store path to file"""
        self.path = path

    @abstractclassmethod
    def find_spec(cls, name, path, target=None):
        """Look for file"""
        pass

    def create_module(self, spec):
        """Returning None uses the standard machinery for creating modules"""
        return None

    @abstractmethod
    def exec_module(self, module):
        """Executing the module means reading the file and updating module __dict__"""
        pass

    def __repr__(self):
        """Nice representation of the class"""
        return f"{self.__class__.__name__}({str(self.path)!r})"