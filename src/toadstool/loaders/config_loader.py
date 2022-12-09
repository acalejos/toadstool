import pathlib
import sys
from importlib.machinery import ModuleSpec
import configparser

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class ConfigLoader(Loader):
    """
    Used to import Json files into a Python dict
    """
    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for Config file"""
        package, _, module_name = name.rpartition(".")
        filename = f"{module_name}.ini"
        directories = sys.path if path is None else path
        for directory in directories:
            path = pathlib.Path(directory) / filename
            if path.exists():
                return ModuleSpec(name, cls(path))

    def exec_module(self, module):
        """Executing the module means reading the gql file"""
        config = configparser.ConfigParser()
        data = config.read(self.path)
        fieldnames = tuple(identifier(key) for key in data.sections())
        fields = dict(zip(fieldnames, data.values()))
        module.__dict__.update(fields)
        module.__dict__["config"] = data
        module.__file__ = str(self.path)
