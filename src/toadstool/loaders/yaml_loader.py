import yaml

from toadstool.utils.utils import identifier
from toadstool.loaders.base_loader import Loader

class YamlLoader(Loader):
    """
    Used to import Yaml files into a Python dict
    """
    file_exts = ["yaml","yml"]

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
