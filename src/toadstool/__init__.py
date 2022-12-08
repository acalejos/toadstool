import sys
import logging
from importlib import import_module

LOG = logging.getLogger("toadstool")
all_loaders= [
    ('toadstool.loaders.gql_loader','GqlLoader','gql'),
    ('toadstool.loaders.json_loader','JsonLoader',None)
]
active_loaders = []

for loader_mod, loader_class, extra_option in all_loaders:
    try:
        module = import_module(loader_mod)
        cls = getattr(module,loader_class)
    except (ImportError, ModuleNotFoundError) as e:
        if extra_option is None:
            raise e
        else:
            LOG.info(f"Running without {extra_option} support. Install with `pip install {__name__}[{extra_option}]")
    else:
        active_loaders.append(cls)

sys.meta_path += active_loaders