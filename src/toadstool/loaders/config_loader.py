import configparser

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class ConfigLoader(Loader):
    """
    Used to import Config files into a Python dict
    """
    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for Config file"""
        return super().find_spec(name,path,target,file_exts="ini")

    def exec_module(self, module):
        """Executing the module means reading the gql file"""
        config = configparser.ConfigParser()
        data = config.read(self.path)
        fieldnames = tuple(identifier(key) for key in data.sections())
        fields = dict(zip(fieldnames, data.values()))
        module.__dict__.update(fields)
        module.__dict__["config"] = data
        super().exec_module(module)
