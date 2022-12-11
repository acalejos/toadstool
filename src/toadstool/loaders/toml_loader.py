try:
    import tomllib as toml
except ImportError:
    import logging
    import sys
    logger = logging.getLogger("toadstool")
    logging.info(f"Current Python Version: {sys.version.split()[0]} is less than required '3.11.0' to use `tomllib` standard library. Reverting to `toml` library")
    import toml

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class TomlLoader(Loader):
    """
    Used to import Toml files into a Python dict
    """
    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for file"""
        return super().find_spec(name,path,target,file_exts="toml")

    def exec_module(self, module):
        """Executing the module means reading the Toml file"""
        with self.path.open() as f:
            data = toml.load(f)
            fieldnames = tuple(identifier(key) for key in data.keys())
            fields = dict(zip(fieldnames, data.values()))
            module.__dict__.update(fields)
        module.__dict__["toml"] = data
        super().exec_module(module)