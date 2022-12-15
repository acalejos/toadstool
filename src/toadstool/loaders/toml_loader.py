try:
    import tomllib as toml
except ImportError:
    import sys
    from toadstool import LOG
    LOG.info("Current Python Version: %s is less than required '3.11.0' to use `tomllib` standard library. Reverting to `toml` library",sys.version.split()[0])
    import toml

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class TomlLoader(Loader):
    """
    Used to import Toml files into a Python dict
    """
    file_exts="toml"

    def exec_module(self, module):
        """Executing the module means reading the Toml file"""
        with self.path.open() as f:
            data = toml.load(f)
        fieldnames = tuple(identifier(key) for key in data.keys())
        fields = dict(zip(fieldnames, data.values()))
        module.__dict__.update(fields)
        module.__dict__["toml"] = data
        super().exec_module(module)