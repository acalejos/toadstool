import pathlib
import sys
from importlib.machinery import ModuleSpec
import json

from toadstool.utils.utils import to_namespace, identifier
from toadstool.loaders.base_loader import Loader

class JsonLoader(Loader):
    """
    Used to import Json files into a Python dict
    """
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

    def exec_module(self, module):
        """Executing the module means reading the gql file"""
        with self.path.open() as f:
            data = json.load(f)
        fieldnames = tuple(identifier(key) for key in data.keys())
        # TODO Does this handle irregular / malformed names from inner json keys?
        fields = dict(zip(fieldnames, [to_namespace(value) for value in data.values()]))
        module.__dict__.update(fields)
        module.__dict__["json"] = data
        module.__file__ = str(self.path)