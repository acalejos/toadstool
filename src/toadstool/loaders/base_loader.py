import pathlib
import sys
from importlib.machinery import ModuleSpec

class Loader():
    """
    Used to import files into a Python dict
    """
    def __init__(self, path):
        """Store path to file"""
        self.path = path

    @classmethod
    def find_spec(cls, name, path, target=None, file_exts: list | str = None) -> ModuleSpec:
        """Look for sfile"""
        package, _, module_name = name.rpartition(".")
        directories = sys.path if path is None else path
        if isinstance(file_exts, list):
            filenames = [f"{module_name}.{ext}" for ext in file_exts]
        elif isinstance(file_exts,str):
            filenames = [f"{module_name}.{file_exts}"]
        else:
            raise ValueError(file_exts)
        for filename in filenames:
            for directory in directories:
                path = pathlib.Path(directory) / filename
                if path.exists():
                    return ModuleSpec(name, cls(path))

    def create_module(self, spec):
        """Returning None uses the standard machinery for creating modules"""
        return None

    def exec_module(self, module):
        """Executing the module means reading the file and updating module __dict__"""
        module.__file__ = str(self.path)

    def __repr__(self):
        """Nice representation of the class"""
        return f"{self.__class__.__name__}({str(self.path)!r})"