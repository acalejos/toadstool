import sys
import logging
from importlib import import_module

LOG = logging.getLogger("toadstool")
all_loaders= [
    ('toadstool.loaders.gql_loader','GqlLoader','gql'),
    ('toadstool.loaders.yaml_loader','YamlLoader','yaml'),
    ('toadstool.loaders.json_loader','JsonLoader',None),
    ('toadstool.loaders.toml_loader','TomlLoader','toml')
]

for loader_mod, loader_class, extra_option in all_loaders:
    try:
        module = import_module(loader_mod)
        cls = getattr(module,loader_class)
    except (ImportError, ModuleNotFoundError):
        if extra_option is not None:
            LOG.info(f"Running without {extra_option} support. Install with `pip install {__name__}[{extra_option}]")
    except AttributeError as e:
        raise e
    else:
        if cls not in sys.meta_path:
            sys.meta_path.append(cls)
