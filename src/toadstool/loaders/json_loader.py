import json

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class JsonLoader(Loader):
    """
    Used to import Json files into a Python dict
    """
    file_exts="json"

    def exec_module(self, module):
        with self.path.open() as f:
            data = json.load(f)
        fieldnames = tuple(identifier(key) for key in data.keys())
        fields = dict(zip(fieldnames, data.values()))
        module.__dict__.update(fields)
        module.__dict__["json"] = data
        super().exec_module(module)
