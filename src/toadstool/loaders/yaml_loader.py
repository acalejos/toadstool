import yaml

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class YamlLoader(Loader):
    """
    Used to import Json files into a Python dict
    """
    @classmethod
    def find_spec(cls, name, path, target=None):
        """Look for file"""
        return super().find_spec(name,path,target,file_exts="yaml")

    def exec_module(self, module):
        """Executing the module means reading the YAML file"""
        with self.path.open() as f:
            docs = list(yaml.safe_load_all(f))
            if len(docs) == 1:
                doc = docs[0]
                fieldnames = tuple(identifier(key) for key in doc.keys())
                fields = dict(zip(fieldnames, doc.values()))
                module.__dict__.update(fields)
        module.__dict__["yaml"] = docs
        super().exec_module(module)
