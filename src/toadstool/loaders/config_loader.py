import configparser

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class ConfigLoader(Loader):
    """
    Used to import Config files into a Python dict
    """
    file_exts=["ini","cfg","config"]

    def exec_module(self, module):
        config = configparser.ConfigParser()
        config.read(self.path)
        fieldnames = tuple(identifier(key) for key in config.sections())
        fields = dict(zip(fieldnames, config._sections.values()))
        module.__dict__.update(fields)
        module.__dict__["config"] = config
        super().exec_module(module)
