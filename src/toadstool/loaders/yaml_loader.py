import pathlib
import sys
from importlib.machinery import ModuleSpec
import yaml

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class YamlLoader(Loader):
    """
    Used to import Json files into a Python dict
    """
    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for Config file"""
        package, _, module_name = name.rpartition(".")
        filename = f"{module_name}.yaml"
        directories = sys.path if path is None else path
        for directory in directories:
            path = pathlib.Path(directory) / filename
            if path.exists():
                return ModuleSpec(name, cls(path))

    def exec_module(self, module):
        """Executing the module means reading the YAML file"""
        with self.path.open() as f:
            docs = list(yaml.safe_load_all(f))
        for doc in docs:
            fieldnames = tuple(identifier(key) for key in doc.keys())
            fields = dict(zip(fieldnames, doc.values()))
            module.__dict__.update(fields)
        module.__dict__["yaml"] = docs
        module.__file__ = str(self.path)
