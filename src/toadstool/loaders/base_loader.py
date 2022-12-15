import pathlib
import sys
from importlib.machinery import ModuleSpec

class Loader:
    """
    Used to import files into a Python dict
    """
    def __init__(self, path):
        """Store path to file"""
        self.path = path

    @classmethod
    @property
    def file_exts(cls) -> str | list[str]:
        """
        Define in the subclass which file extension this Loader should be used for

        Raises:
            NotImplementedError: Raised when subclass does not implement this property
        """
        raise NotImplementedError(f"Class {cls.__name__} must implement attribute 'file_exts'")

    @classmethod
    def find_spec(cls, name, path, target=None) -> ModuleSpec:
        """Look for sfile"""
        package, _, module_name = name.rpartition(".")
        directories = sys.path if path is None else path
        if isinstance(cls.file_exts, list):
            filenames = [f"{module_name}.{ext}" for ext in cls.file_exts]
        elif isinstance(cls.file_exts,str):
            filenames = [f"{module_name}.{cls.file_exts}"]
        else:
            raise ValueError(cls.file_exts)
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