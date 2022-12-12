import json

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class JsonLoader(Loader):
    """
    Used to import Json files into a Python dict
    """
    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for Json file"""
        return super().find_spec(name,path,target,file_exts="json")

    def exec_module(self, module):
        """Executing the module means reading the gql file"""
        with self.path.open() as f:
            data = json.load(f)
        fieldnames = tuple(identifier(key) for key in data.keys())
        fields = dict(zip(fieldnames, data.values()))
        module.__dict__.update(fields)
        module.__dict__["json"] = data
        super().exec_module(module)
