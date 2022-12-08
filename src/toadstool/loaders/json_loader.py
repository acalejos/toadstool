import pathlib
import re
import sys
from importlib.machinery import ModuleSpec
import json

from toadstool.utils.utils import to_namespace

class JsonLoader():
    """
    Used to import Json files into a Python dict
    """
    def __init__(self, path):
        """Store path to Json file"""
        self.path = path

    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for Json file"""
        package, _, module_name = name.rpartition(".")
        filename = f"{module_name}.json"
        directories = sys.path if path is None else path
        for directory in directories:
            path = pathlib.Path(directory) / filename
            if path.exists():
                return ModuleSpec(name, cls(path))

    def create_module(self, spec):
        """Returning None uses the standard machinery for creating modules"""
        return None

    def exec_module(self, module):
        """Executing the module means reading the gql file"""
        with self.path.open() as f:
            data = json.load(f)
        fieldnames = tuple(_identifier(key) for key in data.keys())
        fields = dict(zip(fieldnames, [to_namespace(value) for value in data.values()]))
        module.__dict__.update(fields)
        module.__dict__["json"] = data
        module.__file__ = str(self.path)

    def __repr__(self):
        """Nice representation of the class"""
        return f"{self.__class__.__name__}({str(self.path)!r})"

def _identifier(var_str):
    """Create a valid identifier from a string

    See https://stackoverflow.com/a/3305731
    """
    return re.sub(r"\W|^(?=\d)", "_", var_str)
